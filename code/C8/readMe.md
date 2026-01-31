
诡异现象：我修改了代码，但是没有生效；即便文件里的删除代码，依旧能跑；有一次修改后生效了，但是后面又一直没生效

(myrag) ➜  C8 git:(main) ✗ python /workspace/all-in-rag/code/C8/main.py
.
├── config.py
├── main.py
├── __pycache__
│   └── config.cpython-312.pyc
├── rag_modules
│   ├── data_preparation.py
│   ├── generation_integration.py
│   ├── index_construction.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── data_preparation.cpython-312.pyc
│   │   ├── generation_integration.cpython-312.pyc
│   │   ├── index_construction.cpython-312.pyc
│   │   ├── __init__.cpython-312.pyc
│   │   └── retrieval_optimization.cpython-312.pyc
│   └── retrieval_optimization.py
└── requirements.txt


诡异点2：

  File "/workspace/all-in-rag/code/C8/rag_modules/generation_integration.py", line 41, in setup_llm
    raise ValueError("请设置 MOONSHOT_API_KEY 环境变量")
但是我点击跳转到vscode时过去：实际文件已经修改内容。且文件自动保存

         self.llm = ChatDeepSeek(
            model="deepseek-chat",

【怀疑点】网络存在问题
  - 后续正常



  代码问题：
   - _extract_filters_from_query， 通过关键字过滤。硬编码