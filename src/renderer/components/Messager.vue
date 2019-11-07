<template>
  <div
    class="layout-column messager layout-container"
    v-loading.fullscreen.lock="isLoading"
    element-loading-text="初始化中...请稍后"
  >
    <h3>Messager信息管理</h3>
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item title="发送给今日添加好友" name="1">
        <el-form
          ref="form"
          :inline="false"
          :model="form"
          class="wjp-form"
          label-width="150px"
          label-position="right"
        >
          <el-form-item label="发送给今日添加好友" prop="msg">
            <el-radio-group v-model="form.type" disabled>
              <el-radio :label="3">第一次发送</el-radio>
              <el-radio :label="6">多次发送</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="今日群发时间" prop="msg">
            <el-card class="box-card">
              <div
                v-for="(o,i) in times"
                :key="i"
                class="text item"
              >{{ `时间：${o.time} 发送消息个数：${o.num} 内容：${o.content} `}}</div>
            </el-card>
          </el-form-item>
          <el-form-item>
            <p class="red">（消息只会发送给今天第一次新添加的好友）</p>
          </el-form-item>
          <el-form-item label="群发消息" prop="msg">
            <el-input v-model="form.msg" placeholder="请输入群体发送信息"></el-input>
          </el-form-item>
          <el-form-item class="end">
            <el-button type="primary" v-loading="btnLoading" @click="submit">发 送</el-button>
          </el-form-item>
        </el-form>
      </el-collapse-item>
      <el-collapse-item title="发送给所有好友" name="2">
        <el-form :inline="false" :model="form" class="wjp-form">
          <el-form-item label="群发信息">
            <el-input v-model="form.allMsg" placeholder="请输入要群发的信息"></el-input>
          </el-form-item>
          <el-form-item class="end">
            <el-button type="primary" @click="mass">群 发</el-button>
          </el-form-item>
        </el-form>
      </el-collapse-item>
    </el-collapse>
    <More></More>
  </div>
</template>

<script>
import dayjs from "dayjs";
import More from "@/components/More";
import { userPassSend } from "../api/index.js";
import { setTimeout } from "timers";
import { breakStatement } from "babel-types";
const { ipcRenderer } = require("electron");
export default {
  components: {
    More
  },
  data() {
    return {
      btnLoading: false,
      activeNames: ["1"],
      form: {
        msg: ""
      },
      rules: {
        msg: [{ required: true, message: "请输入发送消息", trigger: "blur" }]
      },
      times: [],
      isLoading: false
    };
  },
  computed: {
    devices() {
      return this.$store.state.Devices.devices;
    }
  },
  created() {
    const times = this.getTime();
    if (
      !!times.length &&
      new dayjs(times[0].time).diff(new dayjs().format("YYYY-MM-DD")) > 0
    ) {
      this.times = this.getTime();
    } else {
      this.times = [];
      localStorage.setItem("messagerTime", JSON.stringify([]));
    }
    this.getDevicesList();
  },
  mounted() {},
  methods: {
    addTime(times) {
      let time = this.getTime();
      let newTime = [...time, times];
      localStorage.setItem("messagerTime", JSON.stringify(newTime));
      this.times = newTime;
    },
    getTime() {
      const times = JSON.parse(localStorage.getItem("messagerTime"));
      return times || [];
    },
    //群发信息
    submit() {
      this.btnLoading = true;
      this.$message({
        message: "正在依次发送，请勿操作！",
        duration: 6000
      });
      userPassSend(this.form.msg)
        .then(res => {
          if (res.success) {
            this.addTime({
              time: new dayjs().format("YYYY-MM-DD HH:mm:ss"),
              content: this.form.msg,
              num: res.data
            });
            this.$refs.form.resetFields();
            this.$message({
              message: "发送成功！",
              type: "success"
            });
          } else {
            this.$message.error("发送失败！");
          }
        })
        .catch(err => {})
        .finally(_ => {
          this.btnLoading = false;
        });
    },
    getDevicesList() {
      this.isLoading = true;
      this.$store.dispatch("getDevicesList").then(devices => {
        this.isLoading = false;
      });
      setTimeout(() => {
        this.isLoading = false;
      }, 1000);
    }
  }
};
</script>
<style lang="scss" scoped>
.messager {
  /deep/.el-collapse-item__header {
    color: #0cbe98;
  }
}
.box-card {
  width: 100%;
  min-width: 200px;
}
/deep/.wjp-form {
  .el-switch {
    margin-bottom: 22px;
    display: flex;
    justify-content: flex-end;
  }
  .end .el-form-item__content {
    justify-content: flex-end;
  }
  .el-form-item__content {
    display: flex;
    .el-input {
      flex: 1;
    }
  }
}
</style>

