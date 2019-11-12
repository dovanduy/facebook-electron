<template>
  <el-drawer title="添加好友" :visible.sync="show" size="400px" :before-close="handleClose">
    <el-form ref="form" :model="config" label-width="100px" size="mini">
      <el-form-item label="账号设备" style="width: 85%">
        <span>{{defaultDevice.fb_nickName || defaultDevice.device_model}}</span>
        <el-divider direction="vertical"></el-divider>
        <span>{{defaultDevice.device_remark || '未设置'}}</span>
      </el-form-item>
      <el-form-item label="搜索词" prop="msg" style="width: 85%">
        <el-input v-model="config.msg" placeholder="搜索关键词"></el-input>
      </el-form-item>
      <el-divider content-position="left">筛选条件</el-divider>
      <el-form-item label="城市" prop="city" style="width: 85%">
        <el-input v-model="config.city" placeholder="城市关键词(请输入英文)"></el-input>
      </el-form-item>
      <el-form-item label="学校" prop="school" style="width: 85%">
        <el-input v-model="config.school" placeholder="学校关键词"></el-input>
      </el-form-item>
      <el-form-item label="公司" prop="work" style="width: 85%">
        <el-input v-model="config.work" placeholder="公司关键词"></el-input>
      </el-form-item>
      <el-divider content-position="left">其他设置</el-divider>
      <el-form-item prop="delay" style="width: 85%">
        <div slot="label">
          <el-popover placement="top-start" trigger="hover" content="每隔多久添加一个好友">
            <span slot="reference">
              添加延时
              <i class="el-icon-question"></i>
            </span>
          </el-popover>
        </div>
        <el-input type="number" v-model="config.sleepTime" placeholder="等待多久添加下一个">
          <template slot="append">秒</template>
        </el-input>
      </el-form-item>
      <el-form-item label="添加人数" prop="num" style="width: 85%">
        <el-input-number v-model="config.num"></el-input-number>
      </el-form-item>
      <el-form-item style="width: 85%">
        <div class="right">
          <el-button type="primary" @click="startAdd">开始</el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-drawer>
</template>

<script>
import { chooseMethod } from "../api/index.js";
import { mapState } from "vuex";
export default {
  name: "AddFriends",
  props: ["show", "defaultDevice"],
  data() {
    return {
      config: {
        msg: "",
        city: null,
        work: null,
        school: null,
        sleepTime: 15,
        num: 5
      }
    };
  },
  computed: {
    ...mapState(["User"])
  },
  methods: {
    handleClose() {
      this.$emit("close");
    },
    startAdd() {
      let data = {
        type: "add_friends",
        params: []
      };
      debugger;
      let config = Object.assign({}, this.config);
      for (let key in config) {
        if (config[key] === null) {
          delete config[key];
        }
      }
      data.params.push(config);
      chooseMethod(
        Object.assign({ userId: this.User.user.userId }, data, {
          equipments: this.defaultDevice.device_id
        })
      ).then(res => {
        // this.$store.dispatch('getDevicesList')
      });
      let myNotification = new Notification(
        this.defaultDevice.device_remark + "正在添加好友",
        {
          body:
            "正在自动添加好友, 请暂时不要操作" +
            this.defaultDevice.device_remark +
            "设备"
        }
      );
      this.handleClose();
    }
  }
};
</script>
