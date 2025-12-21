<script setup>
import { ref, onMounted } from 'vue'
import { backendConfig } from '../api.js'

const emit = defineEmits(['backend-configured'])

const backendUrl = ref('')
const isValid = ref(false)
const isTested = ref(false)
const testMessage = ref('')
const testMessageType = ref('')

// 测试后端连接
const testBackendConnection = async () => {
  if (!backendUrl.value) {
    showTestMessage('请输入后端地址', 'error')
    return
  }

  try {
    // 临时设置URL进行测试
    backendConfig.setUrl(backendUrl.value)
    
    // 测试获取模型列表API
    const response = await fetch(`${backendUrl.value}/api/get_models`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    })
    
    if (response.ok) {
      const data = await response.json()
      showTestMessage('连接成功！后端服务正常运行。', 'success')
      isTested.value = true
      isValid.value = true
    } else {
      showTestMessage(`连接失败: ${response.statusText}`, 'error')
      isTested.value = true
      isValid.value = false
    }
  } catch (error) {
    showTestMessage(`连接失败: ${error.message}`, 'error')
    isTested.value = true
    isValid.value = false
  }
}

// 保存配置
const saveConfig = () => {
  if (!isValid.value) {
    showTestMessage('请先测试后端连接', 'error')
    return
  }
  
  backendConfig.setUrl(backendUrl.value)
  emit('backend-configured')
}

const showTestMessage = (msg, type) => {
  testMessage.value = msg
  testMessageType.value = type
  setTimeout(() => {
    testMessage.value = ''
  }, 5000)
}

// 验证URL格式
const validateUrl = () => {
  const urlPattern = /^https?:\/\/.+/;
  isValid.value = urlPattern.test(backendUrl.value)
  isTested.value = false
}

// 组件加载时检查是否已配置
onMounted(() => {
  if (backendConfig.isConfigured()) {
    backendUrl.value = backendConfig.getUrl()
    isValid.value = true
    isTested.value = true
  }
})
</script>

<template>
  <div class="config-container">
    <div class="config-card">
      <div class="config-header">
        <h2>配置后端服务</h2>
        <p class="subtitle">请输入您本地运行的后端服务地址</p>
      </div>
      
      <div class="form-group">
        <label class="input-label">
          <span class="label-text">后端服务地址</span>
        </label>
        <div class="input-wrapper">
          <span class="input-icon">🌐</span>
          <input 
            type="url" 
            v-model="backendUrl" 
            placeholder="例如: http://localhost:8000" 
            class="config-input"
            :class="{ 'input-valid': isValid && isTested }"
            @input="validateUrl"
          />
        </div>
        <p class="help-text">
          请确保后端服务已在本地启动，通常地址为 http://localhost:8000
        </p>
      </div>

      <div class="button-group">
        <button 
          class="test-btn" 
          @click="testBackendConnection"
          :disabled="!backendUrl"
        >
          测试连接
        </button>
        
        <button 
          class="save-btn" 
          @click="saveConfig"
          :disabled="!isValid || !isTested"
        >
          保存配置
        </button>
      </div>

      <div 
        v-if="testMessage" 
        :class="['test-message', testMessageType]"
        class="test-message"
      >
        <span class="message-icon">{{ testMessageType === 'success' ? '✅' : '❌' }}</span>
        <span class="message-text">{{ testMessage }}</span>
      </div>
      
      <div class="instructions">
        <h3>使用说明</h3>
        <ol>
          <li>在您的电脑上启动后端服务：<br>
            <code>conda activate shixi && cd backend_django && python manage.py runserver 8000</code>
          </li>
          <li>在上面的输入框中输入后端服务地址</li>
          <li>点击"测试连接"验证后端服务是否正常运行</li>
          <li>点击"保存配置"完成后端设置</li>
          <li>配置完成后，您就可以使用YOLOv8检测功能了</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 配置容器 */
.config-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  animation: gradientShift 8s ease infinite;
  background-size: 200% 200%;
}

/* 背景动画 */
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* 配置卡片 */
.config-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 600px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.config-card:hover {
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
  transform: translateY(-5px);
}

/* 配置头部 */
.config-header {
  text-align: center;
  margin-bottom: 30px;
}

.config-header h2 {
  color: #2d3748;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #718096;
  font-size: 16px;
}

/* 表单组 */
.form-group {
  margin-bottom: 25px;
}

/* 输入标签 */
.input-label {
  display: block;
  margin-bottom: 8px;
}

.label-text {
  color: #4a5568;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s ease;
}

/* 输入包装器 */
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

/* 输入图标 */
.input-icon {
  position: absolute;
  left: 12px;
  color: #a0aec0;
  font-size: 16px;
  transition: all 0.3s ease;
  z-index: 1;
}

/* 配置输入框 */
.config-input {
  width: 100%;
  padding: 14px 16px 14px 40px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 15px;
  color: #2d3748;
  background: white;
  transition: all 0.3s ease;
  outline: none;
}

.config-input::placeholder {
  color: #a0aec0;
  transition: all 0.3s ease;
}

.config-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.config-input:focus::placeholder {
  color: #cbd5e0;
}

.config-input.input-valid {
  border-color: #48bb78;
  box-shadow: 0 0 0 3px rgba(72, 187, 120, 0.1);
}

/* 帮助文本 */
.help-text {
  margin-top: 8px;
  font-size: 13px;
  color: #718096;
}

/* 按钮组 */
.button-group {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

/* 测试按钮 */
.test-btn {
  flex: 1;
  padding: 14px 20px;
  background: #f7fafc;
  color: #4a5568;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.test-btn:hover:not(:disabled) {
  background: #edf2f7;
  border-color: #cbd5e0;
}

.test-btn:disabled {
  background: #f7fafc;
  color: #a0aec0;
  border-color: #e2e8f0;
  cursor: not-allowed;
}

/* 保存按钮 */
.save-btn {
  flex: 1;
  padding: 14px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.save-btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  box-shadow: none;
}

/* 测试消息 */
.test-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  text-align: left;
  margin-top: 15px;
  transition: all 0.3s ease;
  animation: slideIn 0.3s ease forwards;
}

.test-message.success {
  background: rgba(72, 187, 120, 0.1);
  color: #22543d;
  border: 1px solid rgba(72, 187, 120, 0.3);
}

.test-message.error {
  background: rgba(239, 68, 68, 0.1);
  color: #742a2a;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.message-icon {
  font-size: 16px;
}

.message-text {
  flex: 1;
}

/* 使用说明 */
.instructions {
  margin-top: 30px;
  padding: 20px;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.instructions h3 {
  color: #2d3748;
  font-size: 16px;
  margin-bottom: 15px;
}

.instructions ol {
  color: #4a5568;
  font-size: 14px;
  line-height: 1.6;
  padding-left: 20px;
}

.instructions li {
  margin-bottom: 10px;
}

.instructions code {
  background: #f7fafc;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 13px;
  color: #2d3748;
  display: block;
  margin-top: 5px;
}

/* 动画 */
@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .config-card {
    padding: 30px 20px;
    margin: 0 10px;
  }
  
  .config-header h2 {
    font-size: 24px;
  }
  
  .button-group {
    flex-direction: column;
  }
}
</style>