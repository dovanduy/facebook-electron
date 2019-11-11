<template>
  <div
    class="layout-column layout-container"
    v-loading.fullscreen.lock="isLoading"
    element-loading-text="初始化中...请稍后"
  >
    <h3>养号商城</h3>
    <div class="box-content">
      <div class="box-header layout-row__between">
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="养号类型">
            <el-select v-model="form.type" placeholder="请选择类型">
              <el-option
                v-for="item in types"
                :key="item.type_id"
                :label="item.label"
                :value="item.type_id"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div class="button">
          <el-button type="primary" @click="search">搜 索</el-button>
        </div>
      </div>
      <div class="box-footer">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="date" label="日期" width="180"></el-table-column>
          <el-table-column prop="name" label="姓名" width="180"></el-table-column>
          <el-table-column prop="address" label="地址"></el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import dayjs from "dayjs";
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
      tableData: [],
      types: []
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
            this.search();
          }
        })
        .catch(err => {});
    },
    search() {
      aKeyHaveNo({
        user_id: this.User.user.userId,
        type_id: this.form.type
      }).then(res => {
        if (res.success) {
          this.tableData = res.data;
        }
      });
    }
  }
};
</script>
<style lang="scss" scoped>
</style>

