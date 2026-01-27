import os
import pandas as pd
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import IndexNode
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

load_dotenv()

# 配置模型
Settings.llm = DeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5")

# 1.加载数据并为每个工作表创建查询引擎和摘要节点
excel_file = '../../data/C3/excel/movie.xlsx'
xls = pd.ExcelFile(excel_file)

df_query_engines = {}
all_nodes = []

print("sheet counts: ", len(xls.sheet_names))
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    # 为当前工作表（DataFrame）创建一个 PandasQueryEngine
    query_engine = PandasQueryEngine(df=df, llm=Settings.llm, verbose=True)
    
    # 为当前工作表创建一个摘要节点（IndexNode）
    year = sheet_name.replace('年份_', '')
    summary = f"这个表格包含了年份为 {year} 的电影信息，可以用来回答关于这一年电影的具体问题。"
    node = IndexNode(text=summary, index_id=sheet_name)
    all_nodes.append(node)
    
    # 存储工作表名称到其查询引擎的映射
    df_query_engines[sheet_name] = query_engine

# 2. 创建顶层索引（只包含摘要节点）
vector_index = VectorStoreIndex(all_nodes)

# 3. 创建递归检索器
# 3.1 创建顶层检索器，用于在摘要节点中检索
vector_retriever = vector_index.as_retriever(similarity_top_k=1)

# 3.2 创建递归检索器
recursive_retriever = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": vector_retriever},
    query_engine_dict=df_query_engines,
    verbose=True,
)

# 4. 创建查询引擎
query_engine = RetrieverQueryEngine.from_args(recursive_retriever)

# 5. 执行查询
query = "1994年与1995年评分人数最少的电影是哪一部？"
print(f"查询: {query}")
response = query_engine.query(query)
print(f"回答: {response}")

"""
INFO:sentence_transformers.SentenceTransformer:Load pretrained SentenceTransformer: BAAI/bge-small-zh-v1.5
Load pretrained SentenceTransformer: BAAI/bge-small-zh-v1.5
INFO:sentence_transformers.SentenceTransformer:1 prompt is loaded, with the key: query
1 prompt is loaded, with the key: query
sheet counts:  27
查询: 1994年评分人数最少的电影是哪一部？
Retrieving with query id None: 1994年评分人数最少的电影是哪一部？
Retrieved node with id, entering: 年份_1994
Retrieving with query id 年份_1994: 1994年评分人数最少的电影是哪一部？
INFO:httpx:HTTP Request: POST https://api.deepseek.com/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.deepseek.com/chat/completions "HTTP/1.1 200 OK"
> Pandas Instructions:
```
df.loc[df['编号'] == 28, '电影名称'].iloc[0]
```
> Pandas Output: 活着
Got response: 活着
INFO:httpx:HTTP Request: POST https://api.deepseek.com/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.deepseek.com/chat/completions "HTTP/1.1 200 OK"
回答: 活着
"""


"""
查询: 1994年与1995年评分人数最少的电影是哪一部

Retrieved node with id, entering: 年份_1994
Retrieving with query id 年份_1994: 1994年与1995年评分人数最少的电影是哪一部？
INFO:httpx:HTTP Request: POST https://api.deepseek.com/chat/completions "HTTP/1.1 200 OK"
HTTP Request: POST https://api.deepseek.com/chat/completions "HTTP/1.1 200 OK"
 - 》：严重问题，内部支持的只有单年份。后续使用 LLM 生成 pands 查询代码，实际上不支持。
      单个df只有一个年份的数据。
> Pandas Instructions:
```
df[(df['编号'].isin([2, 5])) & (df['评分人数'] == df[df['编号'].isin([2, 5])]['评分人数'].min())]['电影名称'].iloc[0]
```

报错：
IndexError: single positional indexer is out-of-bounds
> Pandas Output: There was an error running the output as Python code. Error message: single positional indexer is out-of-bounds

"""