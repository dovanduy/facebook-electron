<template>
  <div
    class="layout-column layout-container"
    v-loading.fullscreen.lock="isLoading"
    element-loading-text="初始化中...请稍后"
  >
    <h3>养号</h3>
    <div class="box-content">
       <p class="red">（养号为长期任务任务哦，请确保手机每天连接！）</p>
      <div class="box-header">
        <div v-for="(item,i) in phone">
          <el-form :inline="true" label-width="80px" :model="form[i]">
            <el-form-item label="设备">
              <p> {{ devices.find(n=>item.id == n.device_id).fb_nickName }} </p>
            </el-form-item>
            <el-form-item label="养号类型">
              <el-select v-model="form[i].typeId" placeholder="请选择">
                <el-option
                  v-for="(v,k) in item.option"
                  :key="k"
                  :label="v"
                  :value="k">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="发帖内容" v-if="form[i].typeId==4">
              <el-input v-model="form[i].postingMsg"></el-input>
            </el-form-item>
            <el-form-item label="点赞个数" v-if="form[i].typeId==4">
              <el-input v-model="form[i].likeNum"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="start(item,i)">开 始</el-button>
            </el-form-item>
          </el-form>
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
      fbNickName:'',
      phone:[],
      form:[{
        typeId:''
      }]
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
            this.phone = []
            let keys = Object.keys(res.data)
            keys.map((k,i)=>{
              this.phone.push({
                id:k,
                option:res.data[k]
              })
            })
            console.log(this.phone)
          }
        })
        .catch(err => {});
    },
    start(data,index) {
      new Notification("养号", {
        body: "养号开始。。。"
      });
      let params = {
        fbNickName: this.devices.find(item=>data.id == item.device_id).fb_nickName,
        typeId: this.form[index].typeId,
        equipments:data.id
      }
      if(this.form[index].typeId == 4){
        params.postingMsg = this.form[index].postingMsg
        params.likeNum = this.form[index].likeNum
      }
      aKeyHaveNo(params)
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

