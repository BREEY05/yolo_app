# YOLO识别系统部署指南

## 项目结构
```
d:/anaconda/envs/shixi/
├── backend_django/          # Django后端
├── YOLO_System/frontend/   # Vue前端
├── docker-compose.yml      # Docker编排文件
└── deploy.sh              # 部署脚本
```

## 服务器信息
- 服务器IP: 154.8.156.58
- 系统: OpenCloudOS 8
- 已安装: Docker 26

## 部署步骤

### 1. 准备项目文件
- 后端Django已配置Dockerfile
- 前端Vue已配置Dockerfile
- 创建了docker-compose.yml编排文件

### 2. 上传项目到服务器
- 将整个项目上传到服务器目录
- 确保包含所有必要的配置文件

### 3. 部署命令
```bash
# 进入项目目录
cd /path/to/project

# 执行部署脚本
chmod +x deploy.sh
./deploy.sh
```

### 4. 访问地址
- 前端: http://154.8.156.58
- 后端API: http://154.8.156.58:8000

## 环境变量
在docker-compose.yml中已配置以下环境变量:
- DEBUG=False
- ALLOWED_HOSTS=154.8.156.58,localhost,127.0.0.1

## 注意事项
1. 确保服务器已安装Docker和Docker Compose
2. 确保防火墙已开放80和8000端口
3. 数据库文件将映射到宿主机，便于备份
4. 媒体文件也将映射到宿主机，便于存储管理