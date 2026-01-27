import os
from llama_index.core.node_parser import SentenceWindowNodeParser, SentenceSplitter
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import MetadataReplacementPostProcessor

# 1. 配置模型
Settings.llm = DeepSeek(model="deepseek-chat", temperature=0.1, api_key=os.getenv("DEEPSEEK_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5") # BAAI/bge-small-en"
Settings.llm = None

# 2. 加载文档
documents = SimpleDirectoryReader(
    input_files=["../../data/C3/pdf/DeepSeek_OCR2_paper.pdf"]
).load_data()

# 3. 创建节点与构建索引
# 3.1 句子窗口索引
node_parser = SentenceWindowNodeParser.from_defaults(
    window_size=3,
    window_metadata_key="window",
    original_text_metadata_key="original_text",
)
sentence_nodes = node_parser.get_nodes_from_documents(documents)
sentence_index = VectorStoreIndex(sentence_nodes)

# 3.2 常规分块索引 (基准)
base_parser = SentenceSplitter(chunk_size=512)
base_nodes = base_parser.get_nodes_from_documents(documents)
base_index = VectorStoreIndex(base_nodes)

# 4. 构建查询引擎
sentence_query_engine = sentence_index.as_query_engine(
    similarity_top_k=2,
    node_postprocessors=[
        MetadataReplacementPostProcessor(target_metadata_key="window")
    ],
)
base_query_engine = base_index.as_query_engine(similarity_top_k=2)

# 5. 执行查询并对比结果
query = "Qwen2-0.5B and CLIP ViT ? compare them?"
print(f"查询: {query}\n")

print("--- 句子窗口检索结果 ---")
window_response = sentence_query_engine.query(query)
print(f"回答: {window_response}\n")

print("--- 常规检索结果 ---")
base_response = base_query_engine.query(query)
print(f"回答: {base_response}\n")


"""
RAG的矛盾:
 - 如果chunk太大，则有很多不相关内容。检索时会有干扰
   - 例子：小说检索时，会检索不到想要的。而是出现很多不相关的排在前面
 - 如果chunk太小。缺乏完整的内容
   - 例子：只有小段内容，旁边缺乏了
窗口的作用：



查询: Qwen2-0.5B and CLIP ViT ? compare them?
 - 》：可以发现窗口检索，精度更加好。比：脚本里手动设置的chunk=500

--- 句子窗口检索结果 ---
回答: Qwen2-0.5B has approximately 500 million parameters, which is comparable 
to CLIP ViT's 300 million parameters, without adding significant computational overhead.

--- 常规检索结果 ---
回答: The provided context does not contain any information comparing Qwen2-0.5B 
and CLIP ViT. The references discuss various technical reports and models, 
including Qwen2.5-VL and Qwen3-VL, but do not mention a "Qwen2-0.5B" model 
or provide any details or comparisons involving CLIP ViT.
"""