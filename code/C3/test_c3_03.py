from llama_index.core import VectorStoreIndex, Document, Settings, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. 配置全局嵌入模型
Settings.embed_model = HuggingFaceEmbedding("BAAI/bge-small-zh-v1.5")

# 2. 创建示例文档
texts = [
    "张三是法外狂徒",
    "LlamaIndex是一个用于构建和查询私有或领域特定数据的框架。",
    "它提供了数据连接、索引和查询接口等工具。"
]
docs = [Document(text=t) for t in texts]

# 3. 创建索引并持久化到本地
index = VectorStoreIndex.from_documents(docs)
persist_path = "./llamaindex_index_store"

# context = StorageContext.from_defaults(persist_dir=persist_path)
index.storage_context.from_defaults(persist_dir=persist_path)

# To disable the LLM entirely, set llm=None.
Settings.llm = None
q = index.as_query_engine()
resp = q.query("法律知识")
print(resp)
print("=" * 40)

# 执行检索
retriever = index.as_retriever()
nodes = retriever.retrieve("LlamaIndex是什么？")

for node in nodes:
    print(node.text)
