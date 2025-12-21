<script setup>
import { ref } from 'vue'
import axios from 'axios'

const API_URL = '/api'
const fileInput = ref(null)
const selectedFile = ref(null)
const savePath = ref('')
const isProcessing = ref(false)
const resultUrl = ref('')
const previewUrl = ref('')

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
    resultUrl.value = ''
    isProcessing.value = false
  }
}

const selectSavePath = async () => {
  try {
    const res = await axios.get(`${API_URL}/select_folder`)
    if (res.data.path) {
      savePath.value = res.data.path
    }
  } catch (e) {
    console.error(e)
  }
}

const startProcessing = async () => {
  if (!selectedFile.value || !savePath.value) {
    alert('请先选择文件和保存位置')
    return
  }

  isProcessing.value = true
  
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  
  try {
    const uploadRes = await axios.post(`${API_URL}/upload_temp`, formData)
    const tempFilename = uploadRes.data.filename
    
    const encodedPath = encodeURIComponent(savePath.value)
    resultUrl.value = `${API_URL}/process_stream/${tempFilename}?save_path=${encodedPath}`
    
  } catch (e) {
    console.error(e)
    alert('开始识别失败')
    isProcessing.value = false
  }
}

const triggerFileInput = () => {
  fileInput.value.click()
}
</script>

<template>
  <div class="file-detection">
    <div class="controls-bar">
      <div class="control-group">
        <button class="action-btn" @click="triggerFileInput">选择文件</button>
        <span class="file-name" v-if="selectedFile">{{ selectedFile.name }}</span>
        <span class="file-name placeholder" v-else>未选择文件</span>
      </div>

      <div class="control-group">
        <button class="action-btn" @click="selectSavePath">选择保存位置</button>
        <input type="text" v-model="savePath" readonly placeholder="保存路径" class="path-input"/>
      </div>

      <div class="control-group">
        <button class="start-btn primary" @click="startProcessing">
          开始识别
        </button>
      </div>
    </div>
    
    <input type="file" ref="fileInput" @change="onFileChange" accept="image/*,video/*" style="display: none" />

    <div class="main-content">
      <div class="panel left-panel">
        <h3>源文件预览</h3>
        <div class="preview-box">
          <img v-if="selectedFile && selectedFile.type.startsWith('image')" :src="previewUrl" alt="Preview" />
          <video v-if="selectedFile && selectedFile.type.startsWith('video')" :src="previewUrl" controls></video>
          <div v-if="!selectedFile" class="empty-state">
              请在上方选择文件
          </div>
        </div>
      </div>

      <div class="panel right-panel">
        <h3>识别结果</h3>
        <div class="preview-box">
          <img v-if="resultUrl" :src="resultUrl" alt="Processing..." />
          <div v-if="!resultUrl" class="empty-state">等待开始...</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.file-detection {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
}

.controls-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  flex-wrap: wrap;
  gap: 15px;
  position: relative;
  z-index: 10;
}

.control-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.action-btn {
  padding: 8px 15px;
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  color: #606266;
  transition: all 0.2s;
}

.action-btn:hover {
  border-color: #409eff;
  color: #409eff;
}

.action-btn:active {
  background-color: #ecf5ff;
  transform: translateY(1px);
}

.file-name {
  color: #606266;
  font-size: 0.9em;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-name.placeholder {
  color: #909399;
  font-style: italic;
}

.path-input {
  padding: 8px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  width: 200px;
  color: #606266;
}

.start-btn {
  padding: 8px 20px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
}

.start-btn:active {
  transform: translateY(1px);
}

.main-content {
  display: flex;
  gap: 20px;
  flex: 1;
  min-height: 0; /* Important for nested flex scrolling/sizing */
}

.panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 8px;
  /* border: 1px solid #ebeef5; */
  overflow: hidden;
}

h3 {
    margin: 0 0 10px 0;
    padding: 10px;
    background: #f5f7fa;
    color: #606266;
    text-align: center;
    font-size: 1em;
    border-bottom: 1px solid #ebeef5;
}

.preview-box {
  flex: 1;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

.preview-box img, .preview-box video {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.empty-state {
  color: #909399;
  font-size: 1em;
}
</style>