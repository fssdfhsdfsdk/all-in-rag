

## git push问题

设置ssh-key之后

1、Git: ssh: connect to host github.com port 22: Connection timed out

你遇到的错误：

```
ssh: connect to host github.com port 22: Connection timed out
```

说明你的电脑 **无法通过 SSH 连接到 GitHub 的默认端口 22**。这通常不是 Git 或配置问题，而是 **网络层被阻断**，常见于以下场景：

---

## 🔍 常见原因

### 1. **公司/学校防火墙或网络策略屏蔽了 SSH（端口 22）**
- 很多企业网络、校园网或公共 Wi-Fi 会**阻止出站的 SSH 连接（端口 22）**，以防止数据外泄或隧道攻击。
- 你在家可能正常，在公司/学校就超时。

### 2. **本地防火墙或安全软件拦截**
- 某些杀毒软件、防火墙（如 Windows Defender 防火墙、第三方安全套件）可能限制了 SSH 出站。

### 3. **ISP（网络运营商）限制**
- 极少数 ISP 会干扰或限速端口 22（尤其在某些地区）。

### 4. **SSH 配置错误（较少见）**
- 如果你自定义了 `~/.ssh/config`，可能配置有误。

---

✅ 解决方案：使用 **HTTPS + Token** 或 **SSH over HTTPS（端口 443）**

```bash
# 查看当前远程地址
git remote -v

# 改为 HTTPS 地址
git remote set-url origin https://github.com/<用户名>/<仓库名>.git

# 下次 push 时，VS Code 会弹窗要求认证：
#   用户名：你的 GitHub 用户名
#   密码：你的 Personal Access Token（不是登录密码！）
```
✅ 获取 GitHub Personal Access Token 的详细步骤
登录你的 GitHub 账号
访问 https://github.com 并登录。
进入 Settings（设置）
点击右上角你的头像 → 选择 Settings。
进入 Developer settings（开发者设置）
在左侧边栏底部，找到并点击 Developer settings。
选择 Personal access tokens
在左侧菜单中，点击 Personal access tokens。
你会看到两个选项：
Tokens (classic)（经典令牌，权限较粗）
Fine-grained tokens（细粒度令牌，权限更精确，推荐新项目使用）
生成新令牌
点击 Generate new token → 选择 Generate new token (classic)（如果你不确定，先用 classic，兼容性更好）

=====

方法2：

1. **测试是否能通过 443 连通 GitHub**：
   ```bash
   ssh -T -p 443 git@ssh.github.com
   ```
   如果返回：
   ```
   Hi <your-username>! You've successfully authenticated...
   ```
   说明可行！

2. **配置 SSH 使用端口 443**  
   编辑或创建 `~/.ssh/config` 文件（Windows 路径通常是 `C:\Users\<你>\.ssh\config`）：

   ```ssh-config
   # GitHub via HTTPS (port 443)
   Host github.com
     HostName ssh.github.com
     Port 443
     User git
     IdentityFile ~/.ssh/id_ed25519    # 或你的私钥路径，如 id_rsa
     IdentitiesOnly yes
   ```

3. **保持远程 URL 为 SSH 格式**：
   ```bash
   git remote set-url origin git@github.com:<用户名>/<仓库名>.git
   ```

4. **现在就可以正常使用 `git push` 了**，SSH 会自动走 443 端口。
