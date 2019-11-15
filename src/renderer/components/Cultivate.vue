<template>
  <div
    class="layout-column layout-container"
    v-loading.fullscreen.lock="isLoading"
    element-loading-text="初始化中...请稍后"
  >
    <h3>养号</h3>
    <div class="box-content">
      <div class="box-header layout-row">
        <el-form ref="form" :inline="true" :model="form" label-width="80px">
          <el-form-item label="养号类型">
            <el-select v-model="form.type" placeholder="请选择类型">
              <el-option v-for="(v,k) in types" :key="k" :label="v" :value="k"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label>
            <p class="red">（养号为长期任务任务哦，请确保手机每天连接！）</p>
          </el-form-item>
        </el-form>
        <div class="button">
          <el-button type="primary" @click="start">开 始</el-button>
        </div>
      </div>
      <div class="box-footer"></div>
    </div>
  </div>
</template>

<script>
const { ipcRenderer } = require("electron");
import { mapState } from "vuex";
import { findHaveNoType, aKeyHaveNo } from "@/api/index";
export default {
  components: {},
  data() {
    return {
      isLoading: false,
      form: {
        type: ""
      },
      types: {}
    };
  },
  computed: {
    ...mapState(["User"]),
    devices() {
      return this.$store.state.Devices.devices;
    }
  },
  created() {
    this.init();
  },
  mounted() {},
  methods: {
    init() {
      findHaveNoType()
        .then(res => {
          if (res.success) {
            this.types = res.data;
            this.form.type = Object.keys(this.types)[0];
          }
        })
        .catch(err => {});
    },
    start() {
      new Notification("养号", {
        body: "批量养号开始。。。"
      });
      aKeyHaveNo({
        user_id: this.User.user.userId,
        type_id: this.form.type
      })
        .then(res => {
          if (res.success) {
            new Notification("养号", {
              body: "" + this.defaultDevice.device_remark + "设备"
            });
          } else {
            new Notification("养号", {
              body: res.msg
            });
          }
        })
        .catch(err => {
          new Notification("养号", {
            body: err.msg
          });
        });
    }
  }
};
</script>
<style lang="scss" scoped>
</style>

