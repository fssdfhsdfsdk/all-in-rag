


## 问题1：补全失败

【问题现象】使用web 云IDE，vscode，发现无法弹出文档提示（现在正在加载），无法在写代码时弹出提示。无法跳转到python库包的位置（有可以的，但是速度极慢）
    - 注意1：代码点击运行，是正常可运行的。 服务器正常、cpu正常、内存、磁盘都正常。
    - 注意2：今天早上还是正常的，后面有问题。



问题诊断：Jedi 语言服务器补全失败
你遇到的错误是 Jedi 语言服务器（VS Code Python 扩展使用的代码补全引擎）在解析 transformers 库中的文件时触发的缓存异常：
```
KeyError: PosixPath('/root/miniconda/envs/myrag/lib/python3.12/site-packages/transformers/models/aimv2/configuration_aimv2.py')
```

#### 根本原因

Jedi 内部维护了一个 **Parso 语法树缓存**（`parser_cache`），用于加速代码分析。当它尝试从缓存中读取 `configuration_aimv2.py` 文件的解析结果时，发现该路径不存在于缓存字典中，从而抛出 `KeyError`。这通常由以下原因导致：

1. **缓存不一致**：Jedi 缓存未及时更新，而 `transformers` 库已被升级或修改。
2. **文件动态生成**：`aimv2` 模型可能是近期新增的，Jedi 启动时尚未加载该模块。
3. **并发冲突**：多个 LSP 请求同时触发缓存读写，导致状态不一致。
4. **路径大小写或符号链接问题**：Linux 系统中路径解析存在细微差异。

> 注：`Cancel notification for unknown message id` 警告是副作用——因主请求失败，VS Code 尝试取消后续请求但找不到对应 ID，属于正常现象，无需单独处理。

解决：web IDE的默认不是 Pylance ，重新安装



## 问题2：webIDE 安装 Pylance

问题1：腾讯云的stuido 插件商场没有 Pylance，需要本地vscode下载。

手动从本地的vscode下载：VXSI包，上传IDE安装

报错：
Error: Unable to install extension 'ms-python.vscode-pylance' as it is not compatible with VS Code '1.95.3'.

注：VS Code 1.95.3 发布于 2024年11月，到 2026年2月已落后 15+ 个版本；Pylance  选择 v2024.11.1（最后兼容 1.95.x 的版本）

这是 Jedi 缓存设计缺陷，在大型库（如 transformers）中高频崩溃
 - 微软已官方弃用 Jedi：VS Code Python 扩展 2026 版默认禁用 Jedi

 解决：下载 ms-python.vscode-pylance-2024.10.104.vsix，安装，后续恢复正常。

