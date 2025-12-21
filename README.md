# YOLOv8 车辆行人检测系统

这是一个基于 **Django** 后端和 **Vue 3** 前端的全栈 Web 应用，集成了 **YOLOv8** 模型，用于实时和离线（文件）的车辆与行人检测。

## 🚀 项目功能

- **用户系统**：支持用户注册、登录及邮箱验证码验证。
- **实时检测**：通过 Web 摄像头进行实时的车辆和行人目标检测。
- **文件检测**：支持上传图片或视频文件进行离线检测并查看结果。
- **模型管理**：支持动态切换不同的 YOLOv8 模型（如 `yolov8n.pt` 等），并支持手动上传新模型。
- **响应式界面**：现代化的 UI 设计，支持用户名显示及退出登录功能。

## 🛠️ 技术栈

### 后端 (Django)
- **核心框架**：Django 4.2.7
- **目标检测**：Ultralytics YOLOv8
- **图像处理**：OpenCV, Pillow
- **接口标准**：REST API (Django Rest Framework)
- **数据库**：SQLite (开发环境)

### 前端 (Vue.js)
- **核心框架**：Vue 3
- **构建工具**：Vite 5
- **通信库**：Axios
- **状态管理**：LocalStorage + Vue ref

## 📁 项目结构

```text
yolo_app/
├── backend/            # Django 后端代码
│   ├── core/           # 核心检测逻辑 (YOLOv8, 摄像头处理)
│   ├── users/          # 用户管理逻辑 (注册, 登录, 验证)
│   ├── yolo_project/   # Django 项目配置
│   ├── models/         # 存放 .pt 模型文件
│   └── manage.py       # Django 管理脚本
├── frontend/           # Vue 3 前端代码
│   ├── src/            # 源代码 (组件, API 配置)
│   ├── package.json    # 前端依赖配置
│   └── vite.config.js  # Vite 配置文件
├── vercel.json         # Vercel 部署配置
└── .vercelignore       # Vercel 忽略文件配置
```

## ⚙️ 本地开发环境配置

### 后端启动
1. 进入 backend 目录：`cd backend`
2. 安装依赖：`pip install -r requirements.txt`
3. 运行迁移：`python manage.py migrate`
4. 启动服务：`python manage.py runserver`

### 前端启动
1. 进入 frontend 目录：`cd frontend`
2. 安装依赖：`npm install`
3. 启动开发服务器：`npm run dev`

## ☁️ 部署说明

项目已配置好 **Vercel** 部署支持：
- **配置文件**：根目录下的 `vercel.json` 自动处理了 Python 运行环境和前端静态文件的构建。
- **构建输出**：前端构建后的文件会自动存放于 `backend/dist` 目录，由 Django 负责托管。

## 📝 许可证

本项目基于 Python 许可证。详细信息请参阅 `LICENSE_PYTHON.txt`。

---
*Created by [BREEY05](https://github.com/BREEY05)*
