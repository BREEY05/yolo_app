<script setup>
import { ref, onMounted } from 'vue'
import { api, backendConfig } from './api.js'
import Login from './components/Login.vue'
import RegisterFixed from './components/RegisterFixed.vue'
import BackendConfig from './components/BackendConfig.vue'
import FileDetection from './components/FileDetection.vue'
import CameraDetection from './components/CameraDetection.vue'

const isLoggedIn = ref(false)
const username = ref('')
const showRegister = ref(false)
const showBackendConfig = ref(false)

const models = ref([])
const currentModel = ref('yolov8n.pt')
const activeTab = ref('file') // 'file' or 'camera'
const fileInput = ref(null)

const handleLoginSuccess = (user) => {
  username.value = user
  isLoggedIn.value = true
  showRegister.value = false
  localStorage.setItem('isLoggedIn', 'true')
  localStorage.setItem('username', user)
  fetchModels()
}

const handleRegisterSuccess = (user) => {
  // 注册成功后切换到登录页面
  showRegister.value = false
}

const switchToRegister = () => {
  console.log('Switching to register page')
  showRegister.value = true
}

const switchToLogin = () => {
  console.log('Switching to login page')
  showRegister.value = false
}

const logout = () => {
  isLoggedIn.value = false
  username.value = ''
  localStorage.removeItem('isLoggedIn')
  localStorage.removeItem('username')
}

const fetchModels = async () => {
  try {
    const res = await api.get('/get_models')
    models.value = res.data.models
    if (!models.value.includes(currentModel.value) && models.value.length > 0) {
      currentModel.value = models.value[0]
    }
  } catch (e) {
    console.error(e)
  }
}

const setModel = async () => {
  try {
    await api.post('/set_model', { model_name: currentModel.value })
    // alert(`已切换模型: ${currentModel.value}`)
  } catch (e) {
    alert('模型切换失败')
  }
}

const triggerUploadModel = () => {
  fileInput.value.click()
}

const uploadModel = async (e) => {
  const file = e.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    await api.post('/upload_model', formData)
    alert('模型上传成功')
    await fetchModels()
    currentModel.value = file.name
    await setModel()
  } catch (e) {
    console.error(e)
    alert('模型上传失败')
  }
}

const handleBackendConfigured = () => {
  showBackendConfig.value = false
  // 加载模型列表
  fetchModels()
}

onMounted(() => {
  // 检查后端是否已配置
  if (!backendConfig.isConfigured()) {
    showBackendConfig.value = true
    return
  }
  
  const savedLogin = localStorage.getItem('isLoggedIn')
  const savedUser = localStorage.getItem('username')
  if (savedLogin === 'true') {
    isLoggedIn.value = true
    username.value = savedUser || ''
    fetchModels()
  }
})
</script>

<template>
  <!-- 后端配置界面 -->
  <BackendConfig 
    v-if="showBackendConfig" 
    @backend-configured="handleBackendConfigured" 
  />
  
  <!-- 登录注册界面 -->
  <div v-else-if="!isLoggedIn">
    <Login 
      v-if="!showRegister" 
      @login-success="handleLoginSuccess" 
      @switch-to-register="switchToRegister"
    />
    <RegisterFixed 
      v-else 
      @register-success="handleRegisterSuccess" 
      @switch-to-login="switchToLogin"
    />
  </div>
  
  <!-- 主应用界面 -->
  <div v-else class="container">
    <header class="card">
      <div class="header-top">
        <h1>YOLOv8 车辆行人检测系统</h1>
        <div class="user-info">
          <span class="welcome-text">欢迎, {{ username }}</span>
          <button class="logout-btn" @click="logout">退出登录</button>
        </div>
      </div>
      <div class="controls-wrapper">
        <div class="controls">
          <label>选择模型:</label>
          <select v-model="currentModel" @change="setModel">
            <option v-for="m in models" :key="m" :value="m">{{ m }}</option>
          </select>
          <button @click="triggerUploadModel">添加模型</button>
          <input 
            type="file" 
            ref="fileInput" 
            @change="uploadModel" 
            accept=".pt" 
            style="display: none" 
          />
        </div>
        
        <div class="tabs">
          <button :class="{ active: activeTab === 'file' }" @click="activeTab = 'file'">文件识别</button>
          <button :class="{ active: activeTab === 'camera' }" @click="activeTab = 'camera'">实时摄像头</button>
        </div>
      </div>
    </header>

    <div class="content card">
      <FileDetection v-if="activeTab === 'file'" />
      <CameraDetection v-if="activeTab === 'camera'" />
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  background: white;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.welcome-text {
  color: #606266;
  font-size: 16px;
  font-weight: 500;
}

.logout-btn {
  padding: 8px 15px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #f78989;
}

h1 {
  margin: 0;
  color: #2c3e50;
  font-size: 2em;
}

.controls-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  width: 100%;
}

.controls {
  display: flex;
  gap: 15px;
  align-items: center;
  justify-content: center;
}

.controls label {
  font-weight: bold;
  color: #606266;
}

.tabs {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.tabs button {
  padding: 10px 30px;
  border: 1px solid #dcdfe6;
  background: white;
  color: #606266;
  border-radius: 20px; /* Rounded pill shape */
}

.tabs button.active {
  background: #409eff;
  color: white;
  border-color: #409eff;
  box-shadow: 0 2px 6px rgba(64, 158, 255, 0.3);
}

.content {
  min-height: 600px;
  background: white;
}
</style>