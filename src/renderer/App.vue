<template>
  <div id="app">
    <div class="drag-header right" style="-webkit-app-region: drag;"></div>
    <div class="header-handle right">
      <i class="icon el-icon-minus" style="margin-right: 5px" @click="miniScreen"></i>
      <i class="icon el-icon-close" @click="closeWin"></i>
    </div>
    <router-view></router-view>
    <p>{{tips }}</p>
    <p>{{downloadPercent }}</p>
  </div>
</template>

<script>
const ipc = require("electron").ipcRenderer;
export default {
  name: "electron-vue",
  data() {
    return {
      tips: false,
      downloadPercent: null,
      scoket: null
    };
  },
  created() {
    ipc.send("update-check");
    ipc.on("update-checking", msg => {
      console.log(msg);
    });
    // 仅在Electron模式下(为了让非Electron后能够正常运行，添加的判断)
    if (process.env.IS_ELECTRON) {
      ipc.on("xxx", () => {
        alert(111);
      });
      return;
      // 发现新版本
      ipc.send("checkForUpdate");
      ipc.on("message", (event, text) => {
        console.log(arguments);
        this.tips = text;
      });
      //注意：“downloadProgress”事件可能存在无法触发的问题，只需要限制一下下载网速就好了
      ipc.on("downloadProgress", (event, progressObj) => {
        console.log(progressObj);
        this.downloadPercent = progressObj.percent || 0;
      });
      ipc.on("isUpdateNow", () => {
        ipc.send("isUpdateNow");
      });
    }
  },
  mounted() {},
  methods: {
    miniScreen() {
      ipc.send("win-mini");
    },
    closeWin() {
      ipc.send("win-close");
    }
  },
  beforeDestroy() {
    // ipc.removeAll(["message", "downloadProgress", "isUpdateNow"]);
  }
};
</script>

<style lang="scss">
/* CSS */
.drag-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 24px;
  z-index: 10;
}
.header-handle {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 36px;
  z-index: 11;
  padding-right: 15px;
  .icon {
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
#app {
  height: 100vh;
}
</style>
