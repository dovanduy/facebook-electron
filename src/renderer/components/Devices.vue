<template>
<div class="devices layout-column" v-loading.fullscreen.lock="isLoading" element-loading-text="初始化中...请稍后">
   <AddGroup
    :defaultDevice="activeDevice"
    :show="isAddGroup" 
    @close="isAddGroup=false"
  />
  <AddFriends
    :defaultDevice="activeDevice"
    :show="isAddFriends" 
    @close="isAddFriends=false"
  />
  <DeviceDetail
    :defaultDevice="activeDevice"
    :show="isDetail" 
    @close="isDetail=false"
  />
  <AddTask
    :defaultDevice="activeDevice"
    :show="isTask"
    @close="isTask=false"
  />
  <div class="device-header layout-row__between" style="width:100%">
    <div style="align-self:center">
      <span>已连接设备 <el-link type="primary">{{devices.length}}</el-link> 台</span>
    </div>
  </div>
  <div class="flex layout-row" style="flex-wrap: wrap;height: 100%;overflow: auto">
    <NoDevice v-show="devices.length === 0"/>
    <el-card
      style="padding: 0;height:430px"
      class="device-screen"
      :class="[activeDevice.device_id === device.device_id ? 'active' : '']"
      v-for="device in devices"
      :key="device.id"
      @click.native="changeActiveDevice(device)"  
    >
      <div class="layout-row__between detail">
        <p>设备备注: {{device.fb_nickName || device.device_remark}}</p>
        <p>状态: <el-link style="font-weight: bold;font-size: 16px" :type="device.device_status === '空闲' ? 'success' : 'danger'">{{device.device_status}}</el-link></p>
      </div>
      <div @click="changeActiveDevice(device)" >
        <webview
          :id="'web' + device.device_id"
          :src="device.for_screen"
          useragent="Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
          style="width:240px;height:397.6px"
          @contextmenu.prevent="showRightMenu(device)"
        ></webview>
      </div>
    </el-card>
  </div>
</div>
</template>

<script>
import AddFriends from "../components/AddFriends";
import AddGroup from "../components/AddGroup";
import NoDevice from "./NoDevice";
import DeviceDetail from "./DeviceDetail";
import AddTask from "./AddTask";
import { getDevices, lockScreen, unlockScreen } from "../api/index.js";
import { setTimeout } from "timers";
import { breakStatement } from "babel-types";
const { ipcRenderer } = require("electron");
export default {
  name: "Devices",
  components: {
    DeviceDetail,
    AddTask,
    NoDevice,
    AddFriends,
    AddGroup
  },
  data() {
    return {
      isAddFriends: false,
      isAddGroup: false,
      isLoading: false,
      activeDevice: {},
      isDetail: false,
      isTask: false
    };
  },
  computed: {
    devices() {
      return this.$store.state.Devices.devices;
    }
  },
  created() {
    this.getDevicesList();
  },
  mounted() {
    // 接收屏幕右键事件
    let self = this;
    ipcRenderer.on("rightMenuEvent", function(event, arg) {
      switch (arg) {
        case "get_detail":
          self.showDetail();
          break;
        case "add_task":
          self.showTask();
          break;
        case "lock":
          self.lock();
          break;
        case "unlock":
          self.unlock();
          break;
        case "add_friends":
          self.isAddFriends = true;
          break;
        case "add_group":
          self.isAddGroup = true;
          break;
      }
    });
  },
  methods: {
    lock() {
      lockScreen(this.activeDevice.device_id).then(res => {
        console.log(res);
      });
    },
    unlock() {
      unlockScreen(this.activeDevice.device_id).then(res => {
        console.log(res);
      });
    },
    changeActiveDevice(device) {
      this.activeDevice = device;
    },
    showTask() {
      this.isTask = true;
    },
    showDetail() {
      this.isDetail = true;
    },
    showRightMenu(device) {
      this.activeDevice = device;
      ipcRenderer.send("showDeviceRightMenu");
    },
    getDevicesList () {
      this.isLoading = true
      this.$store.dispatch('getDevicesList').then((devices) => {
        this.isLoading = false
      })
      setTimeout(() => {
        this.isLoading = false
      }, 1000);
    }
  }
};
</script>

<style>
.el-tab-pane {
  height: 100%;
}
</style>


<style lang="scss" scoped>
.detail {
  font-size: 14px;
  padding: 14px;
  background: #fff;
  border-bottom: 1px solid #ddd;
}
.device-screen{
  width: 240px;
  border: 1px solid #ddd; 
  margin: 10px;
  background: #000;
  border-radius: 10px;
  /deep/ .el-card__body {
    padding: 0;
    width: 100%;
    height: 100%;
  }
}
.device-screen.active {
  border: 5px solid #0cbe98;
}
.devices {
  padding: 0 10px;
  width: 100%;
  height: 100%;
  position: relative;
  z-index: 1;
}
.device-header {
  font-size: 14px;
}
</style>

