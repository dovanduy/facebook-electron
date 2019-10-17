<template>
  <div id="app" v-loading="isLoading" element-loading-text="后端程序下载中...请稍后">
    <div class="drag-header right" style="-webkit-app-region: drag;"></div>
    <div class="header-handle right">
      <i class="icon el-icon-minus" style="margin-right: 5px" @click="miniScreen"></i>
      <i class="icon el-icon-close" @click="closeWin"></i>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
const ipc = require('electron').ipcRenderer;
export default {
  name: 'electron-vue',
  data () {
    return {
      scoket: null,
      isLoading: false
    }
  },
  mounted () {
    let self = this
    ipc.on('backend_update', function (isInstall) {
      if (isInstall) {
        self.isLoading = true
        self.$message.success('文件下载中...请稍后')
      }
    })
    ipc.on('backend_update_success', function (isSuccess) {
      if (isSuccess) {
        self.$message.success('安装成功')
      } else {
        self.$message.error('安装失败，请联系技术人员')
      }
      self.isLoading = false
    })
  },
  methods: {
    miniScreen () {
      ipc.send('win-mini')
    },
    closeWin () {
      ipc.send('win-close')
    }
  }
}
</script>

<style lang="scss">
  /* CSS */
  .drag-header{
    position: absolute;
    top:0;
    left: 0;
    width: 100%;
    height: 24px;
    z-index: 10;
  }
  .header-handle{
    position: absolute;
    top:0;
    left: 0;
    width: 100%;
    height: 36px;
    z-index: 11;
    padding-right: 15px;
    .icon{
      display: inline-block;
      position: relative;
      z-index: 11;
      font-size: 20px;
      line-height: 36px;
      font-weight: bold;
      color: #0cbe98;
      cursor: pointer;
    }
  }
  #app{
    height: 100vh;
  }
</style>
