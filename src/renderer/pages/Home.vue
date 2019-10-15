<template>
<div class="layout-row" style="width:100%;height: 100%">
  <!-- <BanExplain
    :show="showBan" 
    @close="showBan=false"
  /> -->
  <el-tabs class="main-tabs" tab-position="left">
    <ul class="bg-bubbles">
      <li v-for="i in 6" :key="i"></li>
    </ul>
    <el-tab-pane>
      <div slot="label">
        <p class="iconfont icon-shouji"></p>
        <p>设备管理</p>
      </div>
      <Devices></Devices>
    </el-tab-pane>
    <el-tab-pane>
      <div slot="label">
        <p class="el-icon-location" style="font-size:30px;width:100%"></p>
        <p>虚拟定位</p>
      </div>
      <VLoaction></VLoaction>
    </el-tab-pane>
    <el-tab-pane>
      <div slot="label">
        <p class="iconfont icon-facebook1"></p>
        <p>FaceBook</p>
      </div>
    </el-tab-pane>
    <el-tab-pane>
      <div slot="label">
        <p class="iconfont icon-messager"></p>
        <p>Messager</p>
      </div>
    </el-tab-pane>
    <el-tab-pane>
      <div slot="label">
        <p class="iconfont icon-whatsapp"></p>
        <p>WhatsApp</p>
      </div>
    </el-tab-pane>
    <el-tab-pane>
      <div slot="label">
        <p class="iconfont icon-line"></p>
        <p>Line</p>
      </div>
    </el-tab-pane>
    <el-tab-pane>
      <div slot="label">
        <p class="el-icon-s-shop" style="font-size:30px;width:100%"></p>
        <p>账号商城</p>
      </div>
    </el-tab-pane>
  </el-tabs>
</div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
import Devices from '../components/Devices'
import VLoaction from '../components/VLoaction'
// import BanExplain from '../components/BanExplain'
import { breakStatement } from 'babel-types';
const { ipcRenderer } = require('electron')
const path = require('path')
export default {
  name: 'Status',
  data () {
    return {
      showBan: false
    }
  },
  components: {
    Devices,
    // BanExplain,
    VLoaction
  },
  mounted () {
    let self = this
    ipcRenderer.on('socketMsg', function (event, arg) {
      console.log('socket收到消息:' + arg)
      console.log(new Date())
      let data = JSON.parse(arg)
      let type = data.data.type
      let myNotification = null
      let name
      switch (type) {
        case 'insertDevice':
        myNotification = new Notification('接入设备', {
          body: '检测新设备接入系统, 状态更新中...',
          icon: path.join(__dirname, '../assets/images/logo.png')
        })
        self.$store.dispatch('getDevicesList')
        break
        case 'removeDevice':
        myNotification = new Notification('设备断开', {
          body: '检测有设备断开连接, 状态更新中...',
          icon: path.join(__dirname, '../assets/images/logo.png')
        })
        self.$store.dispatch('getDevicesList')
        break
        case 'add_friends':
        let id = data.data.equipments
        let device = self.$store.state.Devices.devices.find((n => n.device_id === id))
        name = device.fb_nickName || device.device_remark || device.device_model
        if (data.msg) {
          myNotification = new Notification('即将开始添加好友', {
            body: `${name}即将在两分钟后开始执行任务, 请暂停操作手机, 等待任务执行完毕...`,
            icon: path.join(__dirname, '../assets/images/logo.png')
          })
        } else {
          myNotification = new Notification('添加好友成功', {
            body: `${name}执行任务完毕...`,
            icon: path.join(__dirname, '../assets/images/logo.png')
          })
        }
        self.$store.dispatch('getDevicesList')
        break
      }
    })
  },
  methods: {
    openBanExplain () {
      this.showBan = true
    },
  }
}
</script>

<style lang="scss">
.bg-bubbles{
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 150px;
  overflow: hidden;
  z-index: 0;
  li {
      position: absolute;
      // bottom 的设置是为了营造出气泡从页面底部冒出的效果；
      // bottom: -160px;
      // 默认的气泡大小；
      width: 40px;
      height: 40px;
      border: 3px solid rgba(232, 251, 255, 1);
      border-radius: 10px;
      // background-color: rgba(232, 251, 255, 1);
      list-style: none;
      // 使用自定义动画使气泡渐现、上升和翻滚；
      animation: square 15s infinite;
      transition-timing-function: linear;
      // 分别设置每个气泡不同的位置、大小、透明度和速度，以显得有层次感；
      &:nth-child(1) {
        left: -10%;
      }
      &:nth-child(2) {
        left: -20%;
        top: 30%;
        animation-delay: 2s;
        animation-duration: 7s;
      }
      &:nth-child(3) {
        left: -25%;
        width: 15px;
        height: 15px;
        top: 40%;
        animation-delay: 4s;
      }
      &:nth-child(4) {
        left: -40%;
        top: 50%;
        width: 25px;
        height: 25px;
        animation-duration: 8s;
        background-color: rgba(255, 255, 255, 0.3);
      }
      &:nth-child(5) {
        left: -70%;
        top: 60%;
      }
      &:nth-child(6) {
        left: -80%;
        top: 70%;
        animation-delay: 3s;
        background-color: rgba(255, 255, 255, 0.2);
      }
      // &:nth-child(7) {
      //   left: -32%;
      //   animation-delay: 2s;
      // }
      // &:nth-child(8) {
      //   left: -55%;
      //   animation-delay: 4s;
      //   animation-duration: 15s;
      // }
      // &:nth-child(9) {
      //   left: -25%;
      //   animation-delay: 2s;
      //   animation-duration: 12s;
      // }
      // &:nth-child(10) {
      //   left: -85%;
      //   animation-delay: 5s;
      // }
    }
    // 自定义 square 动画；
    @keyframes square {
      0% {
        opacity: 0.5;
        transform: translateX(0px) rotate(45deg);
      }
      25% {
        opacity: 0.75;
        transform: translateX(400px) rotate(90deg)
      }
      50% {
        opacity: 1;
        transform: translateX(600px) rotate(135deg);
      }
      100% {
        opacity: 0;
        transform: translateX(1000px) rotate(180deg);
      }
    }
  }
.main-tabs{
  padding-top: 24px;
  width: 100%;
  background: url('../assets/images/bg.png') no-repeat; 
  background-size: 100% 100%;
  .el-tabs__content{
    height: 100%;
  }
  .el-tabs__header{
    box-shadow: 0 10px 12px 0 rgba(0,0,0,.1);
    padding-top: 36px;
  }
  .el-tabs__item{
    margin-bottom: 24px;
    height: auto;
    p{
      text-align: center;
    }
    .iconfont{
      font-size: 30px;
    }
  }
}
.devices{
  flex-wrap: wrap;
}

.el-card__header{
  padding: 0 15px;
  height: 40px;
  line-height: 40px;
}
.devices-list{
  width: 150px;
}
</style>


