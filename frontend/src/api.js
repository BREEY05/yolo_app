// API Configuration
import axios from 'axios';

// 获取当前环境的API基础URL
function getApiBaseUrl() {
  // 开发环境
  if (import.meta.env.DEV) {
    return '/api';
  }
  
  // 生产环境：从本地存储中获取用户设置的后端地址
  const userBackendUrl = localStorage.getItem('userBackendUrl');
  if (userBackendUrl) {
    return userBackendUrl;
  }
  
  // 默认使用相对路径，适配多种访问方式
  return '/api';
}

// 获取或设置后端URL
export const backendConfig = {
  // 获取当前配置的后端URL
  getUrl: () => {
    const url = getApiBaseUrl();
    if (!url) {
      throw new Error('请先配置后端服务地址');
    }
    return url;
  },
  
  // 设置后端URL
  setUrl: (url) => {
    // 去除末尾的斜杠
    const cleanUrl = url.replace(/\/$/, '');
    localStorage.setItem('userBackendUrl', cleanUrl);
  },
  
  // 检查是否已配置 - 总是返回true，因为默认使用 '/api' URL
  isConfigured: () => {
    return true;
  }
};

// 导出axios实例，动态配置baseURL
export const api = axios.create({
  timeout: 30000, // 30秒超时
  withCredentials: true, // 携带凭证
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器：动态设置baseURL
api.interceptors.request.use(config => {
  try {
    const baseUrl = backendConfig.getUrl();
    // 如果URL已经是绝对路径，则不添加baseURL
    if (config.url.startsWith('http')) {
      return config;
    }
    // 添加动态baseURL
    config.baseURL = baseUrl;
    return config;
  } catch (error) {
    console.error('API配置错误:', error.message);
    return Promise.reject(error);
  }
});

// 响应拦截器：处理错误
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // 未授权，清除登录状态
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('username');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

// 默认导出
export default api;