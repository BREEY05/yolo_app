<script setup>
import { ref } from 'vue'
import { api } from '../api.js'

const emit = defineEmits(['register-success', 'switch-to-login'])

const username = ref('')
const email = ref('')
const code = ref('') // Empty by default
const password = ref('')
const isSending = ref(false)
const message = ref('')
const messageType = ref('') // 'success' or 'error'
// UI交互变量
const usernameFocused = ref(false)
const emailFocused = ref(false)
const codeFocused = ref(false)
const passwordFocused = ref(false)
const btnHover = ref(false)

const sendCode = async () => {
  if (!email.value) {
    showMessage('请输入邮箱', 'error')
    return
  }
  
  console.log('Sending verification code to:', email.value)
  
  isSending.value = true
  try {
    const res = await api.post('/users/send_code/', { email: email.value })
    console.log('Verification code response:', res.data)
    if (res.data.status === 'success') {
      showMessage('验证码已发送，请查收邮件', 'success')
    } else {
      showMessage(res.data.message, 'error')
    }
  } catch (e) {
    console.error('Send code error:', e)
    if (e.response) {
      console.error('Response data:', e.response.data)
      showMessage(e.response.data.message || '发送失败，请检查网络或邮箱', 'error')
    } else {
      showMessage('发送失败，请检查网络或邮箱', 'error')
    }
  } finally {
    isSending.value = false
  }
}

const register = async () => {
  if (!username.value || !email.value || !code.value || !password.value) {
    showMessage('请填写完整信息', 'error')
    return
  }

  const requestData = { 
    username: username.value,
    email: email.value,
    code: code.value,
    password: password.value
  }
  
  console.log('Sending registration request:', requestData)

  try {
    // Use api to ensure cookies are properly handled
    const res = await api.post('/users/register/', requestData)
    console.log('Registration response:', res.data)
    
    if (res.data.status === 'success') {
      showMessage('注册成功，请登录', 'success')
      setTimeout(() => {
        emit('register-success', res.data.username)
      }, 1500)
    } else {
      showMessage(res.data.message || '注册失败', 'error')
    }
  } catch (e) {
    console.error('Registration error:', e)
    if (e.response) {
      console.error('Response data:', e.response.data)
      showMessage(e.response.data.message || '注册失败', 'error')
    } else {
      showMessage('注册失败，请重试', 'error')
    }
  }
}

const showMessage = (msg, type) => {
  message.value = msg
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

const switchToLogin = () => {
  emit('switch-to-login')
}
</script>

<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>用户注册</h2>
        <p class="subtitle">创建账户使用YOLOv8检测系统</p>
      </div>
      
      <div class="form-group">
        <label class="input-label">
          <span class="label-text">用户名</span>
        </label>
        <div class="input-wrapper">
          <span class="input-icon">👤</span>
          <input 
            type="text" 
            v-model="username" 
            placeholder="请输入用户名" 
            class="register-input"
            :class="{ 'input-focused': usernameFocused }"
            @focus="usernameFocused = true"
            @blur="usernameFocused = false"
          />
        </div>
      </div>
      
      <div class="form-group">
        <label class="input-label">
          <span class="label-text">QQ 邮箱</span>
        </label>
        <div class="input-row">
          <div class="input-wrapper">
            <span class="input-icon">📧</span>
            <input 
              type="email" 
              v-model="email" 
              placeholder="请输入QQ邮箱" 
              class="register-input"
              :class="{ 'input-focused': emailFocused }"
              @focus="emailFocused = true"
              @blur="emailFocused = false"
            />
          </div>
          <button 
            :disabled="isSending" 
            @click="sendCode"
            class="code-btn"
            :class="{ 'sending': isSending }"
          >
            {{ isSending ? '发送中...' : '获取验证码' }}
          </button>
        </div>
      </div>
      
      <div class="form-group">
        <label class="input-label">
          <span class="label-text">验证码</span>
        </label>
        <div class="input-wrapper">
          <span class="input-icon">🔑</span>
          <input 
            type="text" 
            v-model="code" 
            placeholder="请输入验证码" 
            class="register-input"
            :class="{ 'input-focused': codeFocused }"
            @focus="codeFocused = true"
            @blur="codeFocused = false"
          />
        </div>
      </div>
      
      <div class="form-group">
        <label class="input-label">
          <span class="label-text">密码</span>
        </label>
        <div class="input-wrapper">
          <span class="input-icon">🔒</span>
          <input 
            type="password" 
            v-model="password" 
            placeholder="请输入密码" 
            class="register-input"
            :class="{ 'input-focused': passwordFocused }"
            @focus="passwordFocused = true"
            @blur="passwordFocused = false"
          />
        </div>
      </div>

      <div 
        v-if="message" 
        :class="['message', messageType]"
        class="message"
      >
        <span class="message-icon">{{ messageType === 'success' ? '✅' : '❌' }}</span>
        <span class="message-text">{{ message }}</span>
      </div>

      <button 
        class="register-btn" 
        @click="register"
        :class="{ 'btn-hover': btnHover }"
        @mouseenter="btnHover = true"
        @mouseleave="btnHover = false"
      >
        注 册
      </button>
      
      <div class="switch-form">
        <span>已有账户？</span>
        <button class="switch-btn" @click="switchToLogin">立即登录</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 注册容器 */
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  animation: gradientShift 8s ease infinite;
  background-size: 200% 200%;
}

/* 背景动画 */
@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* 注册卡片 */
.register-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 420px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.register-card:hover {
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
  transform: translateY(-5px);
}

/* 注册头部 */
.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
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
  font-size: 14px;
}

/* 表单组 */
.form-group {
  margin-bottom: 25px;
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
  transform: translateY(20px);
}

.form-group:nth-child(2) {
  animation-delay: 0.1s;
}

.form-group:nth-child(3) {
  animation-delay: 0.2s;
}

.form-group:nth-child(4) {
  animation-delay: 0.3s;
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

/* 输入行 */
.input-row {
  display: flex;
  gap: 12px;
  align-items: stretch;
}

/* 输入包装器 */
.input-wrapper {
  flex: 1;
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

/* 注册输入框 */
.register-input {
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

.register-input::placeholder {
  color: #a0aec0;
  transition: all 0.3s ease;
}

.register-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.register-input:focus::placeholder {
  color: #cbd5e0;
}

.register-input:focus + .input-icon {
  color: #667eea;
  transform: scale(1.1);
}

.input-focused .input-icon {
  color: #667eea;
}

/* 验证码按钮 */
.code-btn {
  padding: 0 20px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  min-width: 120px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.code-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.code-btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  box-shadow: none;
  opacity: 0.7;
}

.code-btn.sending {
  background: #48bb78;
  box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
}

/* 注册按钮 */
.register-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 15px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 15px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  animation: fadeInUp 0.6s ease 0.4s forwards;
  opacity: 0;
  transform: translateY(20px);
}

.register-btn:hover,
.register-btn.btn-hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
}

.register-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* 切换表单 */
.switch-form {
  margin-top: 20px;
  text-align: center;
  color: #718096;
  font-size: 14px;
  animation: fadeInUp 0.6s ease 0.5s forwards;
  opacity: 0;
  transform: translateY(20px);
}

.switch-btn {
  background: none;
  border: none;
  color: #667eea;
  font-weight: 500;
  cursor: pointer;
  margin-left: 5px;
  transition: all 0.3s ease;
  text-decoration: underline;
}

.switch-btn:hover {
  color: #5a67d8;
}

/* 消息提示 */
.message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  text-align: left;
  margin-bottom: 15px;
  transition: all 0.3s ease;
  animation: slideIn 0.3s ease forwards;
  opacity: 0;
  transform: translateY(-10px);
}

.message.success {
  background: rgba(72, 187, 120, 0.1);
  color: #22543d;
  border: 1px solid rgba(72, 187, 120, 0.3);
}

.message.error {
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

/* 动画 */
@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 480px) {
  .register-card {
    width: 90%;
    padding: 30px 24px;
    margin: 0 10px;
  }
  
  .register-header h2 {
    font-size: 24px;
  }
  
  .input-row {
    flex-direction: column;
  }
  
  .code-btn {
    min-height: 48px;
  }
}

@media (max-width: 360px) {
  .register-card {
    padding: 25px 20px;
  }
  
  .register-input {
    padding: 12px 14px 12px 36px;
    font-size: 14px;
  }
}
</style>