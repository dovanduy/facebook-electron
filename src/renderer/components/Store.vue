<template>
  <div
    class="layout-column layout-container"
    v-loading.fullscreen.lock="isLoading"
    element-loading-text="初始化中...请稍后"
  >
    <h3>账号商城</h3>
    <el-tabs v-model="activeName">
      <el-tab-pane label="新号(白号)" name="1">
        <el-table
          ref="table1"
          :data="tableData1"
          tooltip-effect="dark"
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column prop="time" label="注册日期"></el-table-column>
          <el-table-column prop="acount" label="账号"></el-table-column>
          <el-table-column prop="address" label="注册地址" show-overflow-tooltip></el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="周号" name="2">
        <el-table
          ref="table2"
          :data="tableData2"
          tooltip-effect="dark"
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column prop="time" label="注册日期"></el-table-column>
          <el-table-column prop="acount" label="账号"></el-table-column>
          <el-table-column prop="address" label="注册地址" show-overflow-tooltip></el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="月号" name="3">
        <el-table
          ref="table3"
          :data="tableData4"
          tooltip-effect="dark"
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column prop="time" label="注册日期"></el-table-column>
          <el-table-column prop="acount" label="账号"></el-table-column>
          <el-table-column prop="address" label="注册地址" show-overflow-tooltip></el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import dayjs from "dayjs";
const { ipcRenderer } = require("electron");
export default {
  components: {},
  data() {
    return {
      tableData1: [],
      tableData2: [],
      tableData3: [],
      activeName: "1"
    };
  },
  computed: {
    devices() {
      return this.$store.state.Devices.devices;
    }
  },
  created() {},
  mounted() {},
  methods: {}
};
</script>
<style lang="scss" scoped>
</style>

