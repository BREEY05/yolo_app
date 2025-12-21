# YOLOv8 前端部署指南

本指南说明如何将YOLOv8检测系统的前端部署到服务器上，使用户可以通过浏览器访问界面，而计算在用户本地进行。

## 部署架构

```
用户浏览器 <---> 服务器上的前端界面 <---> 用户本地的后端服务
```

- 前端界面部署在服务器上，提供用户界面
- 后端服务运行在用户本地电脑上，负责计算
- 文件操作（选择、保存）都在用户本地进行

## 部署步骤

### 1. 构建前端应用

在 `frontend` 目录下执行：

```bash
# 安装依赖
npm install

# 构建生产版本
npm run build
```

构建完成后，`dist` 目录包含所有需要部署的文件。

### 2. 使用Docker部署（推荐）

在 `frontend` 目录下执行：

```bash
# 使用Docker Compose部署
docker-compose up -d
```

这将启动一个Nginx服务器在8080端口上提供前端服务。

### 3. 直接使用Nginx部署

如果没有Docker，可以直接使用Nginx：

```bash
# 安装Nginx
sudo apt-get install nginx  # Ubuntu/Debian
sudo yum install nginx  # CentOS/RHEL

# 复制构建产物到Nginx目录
sudo cp -r dist/* /var/www/html/

# 复制Nginx配置
sudo cp nginx.conf /etc/nginx/sites-available/yolo-system
sudo ln -s /etc/nginx/sites-available/yolo-system /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# 重启Nginx
sudo systemctl restart nginx
```

### 4. 使用其他Web服务器

也可以使用Apache、Caddy等其他Web服务器，只需要将`dist`目录内容作为网站根目录即可。

## 用户使用流程

1. **访问前端界面**：用户通过浏览器访问服务器上的前端地址（如：http://your-server.com）

2. **配置后端地址**：
   - 首次访问时，会显示"配置后端服务"页面
   - 用户需要输入本地运行的后端服务地址（通常是 http://localhost:8000）
   - 系统会测试连接是否成功
   - 配置成功后，用户界面会显示登录页面

3. **启动本地后端**：
   - 用户需要在本地电脑上启动后端服务：
   ```bash
   conda activate shixi
   cd backend_django
   python manage.py runserver 8000
   ```

4. **使用系统**：
   - 用户注册/登录账户
   - 使用文件上传或实时摄像头进行检测
   - 所有文件操作都在用户本地进行

## 注意事项

1. **CORS配置**：后端需要允许来自前端服务器的跨域请求

2. **网络访问**：确保用户的电脑可以访问服务器上的前端，同时前端可以连接到用户本地后端

3. **文件路径**：系统设计为所有文件操作都在用户本地进行，不会上传到服务器

4. **数据安全**：所有计算和数据都在用户本地处理，服务器只提供界面

## 技术实现

1. **动态后端地址**：
   - 前端通过`api.js`模块管理后端地址
   - 用户配置的后端地址保存在浏览器本地存储中
   - 所有API请求都动态指向用户配置的地址

2. **本地文件处理**：
   - 文件选择和保存都在用户本地进行
   - 使用浏览器原生文件API实现本地文件操作

3. **跨域请求**：
   - 使用CORS和凭证传递实现前端与用户本地后端的通信

## 故障排除

1. **连接后端失败**：
   - 确保用户已启动本地后端服务
   - 检查后端地址是否正确（通常为 http://localhost:8000）
   - 确认防火墙设置允许连接

2. **文件操作失败**：
   - 确保浏览器有文件访问权限
   - 检查文件路径是否有效

3. **CORS错误**：
   - 检查后端CORS配置是否包含前端服务器地址
   - 确保请求包含必要的凭证

## 更新部署

要更新前端应用：

1. 修改代码后重新构建：
   ```bash
   npm run build
   ```

2. 如果使用Docker：
   ```bash
   docker-compose down
   docker-compose up --build -d
   ```

3. 如果直接使用Web服务器：
   ```bash
   sudo cp -r dist/* /var/www/html/
   ```