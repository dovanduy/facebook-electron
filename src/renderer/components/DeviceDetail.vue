<template>
<el-drawer
  title="当前设备账号信息"
  :visible.sync="show"
  size="400px"
  @open="resetData"
  :before-close="handleClose">
  <el-form ref="form" :model="config" label-width="150px" size="mini">
    <el-divider content-position="left">设备信息</el-divider>
    <el-form-item label="设备ID" style="width: 85%">
      <span>{{defaultDevice.device_id}}</span>
    </el-form-item>
    <el-form-item label="设备状态" style="width: 85%">
      <el-link :type="defaultDevice.device_status === '空闲' ? 'success' : 'error'">{{defaultDevice.device_status}}</el-link>
    </el-form-item>
    <el-form-item label="备注名" prop="device_remark" style="width: 85%">
      <el-input v-model="config.device_remark" placeholder="请输入备注名，注意不要重复"></el-input>
    </el-form-item>
    <el-divider content-position="left">账号信息</el-divider>
    <el-form-item label="FaceBook账号标识" prop="fb_nickName" style="width: 85%">
      <el-input v-model="config.fb_nickName" placeholder="请输入FaceBook标识，如名称等"></el-input>
    </el-form-item>
    <el-form-item label="当日添加好友" style="width: 85%">
      <span>{{defaultDevice.friendNum}}</span>
    </el-form-item>
    <el-form-item label="当日添加小组" style="width: 85%">
      <span>{{defaultDevice.treamNum}}</span>
    </el-form-item>
    <el-form-item style="width: 85%">
      <div class="right">
        <el-button type="primary" @click="update">确定</el-button>
      </div>
    </el-form-item>
  </el-form>
</el-drawer>
</template>

<script>
import axios from 'axios'
import { updateDevice } from '../api/index.js'
const { ipcRenderer } = require('electron')
export default {
  name: 'DeviceDetail',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    defaultDevice: {
      type: Object,
      default: () => {}
    },
  },
  data () {
    return {
      config: {
        device_remark: '',
        fb_nickName: ''
      }
    }
  },
  methods: {
    resetData () {
      this.config.device_remark = this.defaultDevice.device_remark || ''
      this.config.fb_nickName = this.defaultDevice.fb_nickName || ''
    },
    handleClose () {
      this.$emit('close')
    },
    update () {
      let data = {
        "device_id": this.defaultDevice.device_id,
        "remark": this.config.device_remark,
        "fbNick": this.config.fb_nickName
      }
      updateDevice(data).then(res => {
        if (res.success) {
          this.$message.success('更新成功')
          this.$store.dispatch('getDevicesList')
          this.handleClose()
        }
      })
    }
  }
}
</script>
