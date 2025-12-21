<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const API_URL = '/api'
const cameras = ref([])
const selectedCamera = ref(null)
const isStreaming = ref(false)
const streamUrl = ref('')
const logs = ref([])

const addLog = (msg) => {
  const time = new Date().toLocaleTimeString()
  logs.value.unshift(`[${time}] ${msg}`)
  if (logs.value.length > 2) logs.value.pop() // Keep only recent 2 logs
}

const fetchCameras = async () => {
  try {
    const res = await axios.get(`${API_URL}/get_cameras`)
    cameras.value = res.data.cameras
    if (cameras.value.length > 0) {
      selectedCamera.value = cameras.value[0].id
      addLog(`找到 ${cameras.value.length} 个摄像头`)
    } else {
      addLog('未找到摄像头')
    }
  } catch (e) {
    console.error(e)
    addLog('连接后台失败: ' + (e.response?.data?.message || e.message))
  }
}

const startStream = () => {
  if (selectedCamera.value === null) return
  streamUrl.value = `${API_URL}/camera_feed/${selectedCamera.value}`
  isStreaming.value = true
  addLog('摄像头已开启')
}

const stopStream = () => {
  streamUrl.value = ''
  isStreaming.value = false
  addLog('摄像头已关闭')
}

onMounted(() => {
  fetchCameras()
})

onUnmounted(() => {
  stopStream()
})
</script>

<template>
  <div class="camera-detection">
    <!-- Top Controls Bar -->
    <div class="top-controls">
      <!-- Input (Select) -->
      <div class="select-wrapper">
        <label>摄像头:</label>
        <select v-model="selectedCamera">
          <option v-for="cam in cameras" :key="cam.id" :value="cam.id">
            {{ cam.name }}
          </option>
        </select>
      </div>

      <!-- Button (Refresh) -->
      <button @click="fetchCameras" class="refresh-btn">刷新</button>

      <!-- Button (Start/Stop) -->
      <button v-if="!isStreaming" class="start-btn primary" @click="startStream">开启</button>
      <button v-else class="stop-btn" @click="stopStream">关闭</button>

      <!-- Span (Status) -->
      <span v-if="isStreaming" class="status-indicator active">运行中</span>
      <span v-else class="status-indicator inactive">已停止</span>
    </div>

    <!-- Log Panel -->
    <div v-if="logs.length > 0" class="log-panel">
      <div v-for="(log, index) in logs" :key="index" class="log-item">{{ log }}</div>
    </div>

    <div class="viewport">
      <div class="video-box">
        <img v-if="isStreaming" :src="streamUrl" alt="Camera Feed" />
        <div v-if="!isStreaming" class="placeholder">请在上侧选择并开启摄像头</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.camera-detection {
  display: flex;
  flex-direction: column;
  gap: 15px;
  height: 100%;
}

.top-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.select-wrapper {
  display: flex;
  align-items: center;
  gap: 5px;
}

.select-wrapper label {
  font-weight: bold;
  color: #333;
}

.select-wrapper select {
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button {
  padding: 5px 15px;
  border-radius: 4px;
  border: 1px solid #ccc;
  cursor: pointer;
  background: white;
}

.start-btn {
  background-color: #42b883;
  color: white;
  border-color: #42b883;
}

.stop-btn {
  background-color: #f56c6c;
  color: white;
  border-color: #f56c6c;
}

.status-indicator {
  font-size: 0.9em;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
  margin-left: auto; /* Push to right or keep near buttons depending on preference */
}

.status-indicator.active {
  background-color: #e1f3d8;
  color: #67c23a;
}

.status-indicator.inactive {
  background-color: #f4f4f5;
  color: #909399;
}

.viewport {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  min-height: 400px;
  position: relative;
}

.video-box {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.status-overlay {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0, 0, 0, 0.6);
  color: #00ff00;
  padding: 5px 10px;
  border-radius: 4px;
  font-weight: bold;
  z-index: 10;
}

.video-box img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.placeholder {
  color: #fff;
  font-size: 1.5em;
  opacity: 0.5;
}
.start-btn {
  background-color: #42b883;
}

.stop-btn {
  background-color: #f56c6c;
  color: white;
  border-color: #f56c6c;
}

.stop-btn:hover {
    background-color: #f78989;
}
</style>