<template>
    <div class="flex flex-col items-center justify-center min-h-screen bg-white p-4">
      <div class="w-full max-w-3xl p-8 bg-white rounded-lg shadow-md">
        <textarea
          v-model="userInput"
          @keyup.enter="getReply"
          placeholder="请输入您的问题..."
          class="w-full p-4 mb-6 text-lg text-gray-700 border rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-400"
          rows="6"
        ></textarea>
        <button
          @click="getReply"
          class="w-full py-3 text-lg font-semibold text-white bg-teal-500 rounded-lg hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:ring-opacity-50 transition-colors duration-200"
        >
          获取回复
        </button>
        <div v-if="reply" class="mt-8 p-6 bg-gray-100 rounded-lg relative">
          <p class="text-gray-800 text-lg">{{ reply }}</p>
          <button
            @click="copyReply"
            class="absolute top-4 right-4 p-2 text-sm bg-teal-500 text-white rounded hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-teal-400 focus:ring-opacity-50 transition-colors duration-200"
          >
            复制
          </button>
        </div>
      </div>
      <!-- 提示信息 -->
      <div 
        v-if="showCopyMessage" 
        class="fixed bottom-8 left-1/2 transform -translate-x-1/2 bg-teal-500 text-white px-6 py-3 rounded-lg shadow-lg transition-opacity duration-300 text-lg"
        :class="{ 'opacity-0': fadeOut }"
      >
        回复已复制到剪贴板
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const userInput = ref('')
  const reply = ref('')
  const showCopyMessage = ref(false)
  const fadeOut = ref(false)
  
  async function getReply() {
    if (!userInput.value.trim()) return
  
    try {
      const response = await fetch('https://info.myron-moshui.online/openai/getReply', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: userInput.value }),
      })
  
      const result = await response.json()
  
      if (result.success) {
        reply.value = result.data.content
      } else {
        reply.value = '获取回复失败，请重试。'
      }
    } catch (error) {
      console.error('Error:', error)
      reply.value = '发生错误，请稍后重试。'
    }
  
    userInput.value = ''
  }
  
  function copyReply() {
    if (reply.value) {
      navigator.clipboard.writeText(reply.value).then(() => {
        showCopyMessage.value = true
        fadeOut.value = false
        
        setTimeout(() => {
          fadeOut.value = true
        }, 2000)
  
        setTimeout(() => {
          showCopyMessage.value = false
        }, 3000)
      }).catch(err => {
        console.error('复制失败:', err)
        alert('复制失败，请手动复制')
      })
    }
  }
  </script>