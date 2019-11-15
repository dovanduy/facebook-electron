<template>
  <div class="no-devices layout-row">
    <div style="width: 60%" class="layout-column__between">
      <div>
        <div class="layout-row align-center" style="margin-bottom: 20px;">
          <h3 style="font-size: 20px;font-weight: bold;">未检测到设备，请确认安卓设备是否连接</h3>
          <el-tooltip class="item" effect="dark" content="刷新设备" placement="top">
            <i class="el-icon-refresh pointer font-16" @click="refresh"></i>
          </el-tooltip>
        </div>
        <p style="font-size: 14px;color: #999">海外智能营销软件——xx科技</p>
        <el-divider></el-divider>
      </div>
      <div class="layout-column__around flex">
        <p class="layout-row">
          <i class="iconfont icon-dingshirenwu" style="font-size: 60px;color: #8ee2d2"></i>
          <span class="layout-column" style="align-self:center;margin-left: 30px;">
            <span style="font-weight: 600;margin-bottom: 10px">定时任务</span>
            <span
              style="color: #999;font-size: 14px;"
            >设定关键词、筛选条件自动执行，做到24 * 7自动添加好友/群，做到真正自动化；全部真机操作，将封号风险降到最低</span>
          </span>
        </p>
        <p class="layout-row">
          <i class="el-icon-location" style="font-size: 60px;color: #62daf4"></i>
          <span class="layout-column" style="align-self:center;margin-left: 30px;">
            <span style="font-weight: 600;margin-bottom: 10px">虚拟定位</span>
            <span style="color: #999;font-size: 14px;">使用虚拟定位功能，让FaceBook主动推荐更多潜在客户！</span>
          </span>
        </p>
        <p class="layout-row">
          <i class="el-icon-s-shop" style="font-size: 60px;color: #0cbe98"></i>
          <span class="layout-column" style="align-self:center;margin-left: 30px;">
            <span style="font-weight: 600;margin-bottom: 10px">账号商城(开发中)</span>
            <span style="color: #999;font-size: 14px;">Facebook、Line等已养账号，可定制养号</span>
          </span>
        </p>
        <p class="layout-row">
          <i class="iconfont icon-fenxi" style="font-size: 60px;color: #8ee2d2"></i>
          <span class="layout-column" style="align-self:center;margin-left: 30px;">
            <span style="font-weight: 600">好友/小组管理分析(开发中)</span>
            <span style="color: #999">......</span>
          </span>
        </p>
        <p class="layout-row">
          <i class="iconfont icon-liaotian1" style="font-size: 60px;color: #f8dbae"></i>
          <span class="layout-column" style="align-self:center;margin-left: 30px;">
            <span style="font-weight: 600">智能聊天回复(开发中)</span>
            <span style="color: #999">......</span>
          </span>
        </p>
        <p class="layout-row">
          <i class="iconfont icon-gengduo" style="font-size: 60px;color: #0cbe98"></i>
          <span class="layout-column" style="align-self:center;margin-left: 30px;">
            <span style="font-weight: 600">更多功能开发中</span>
            <span style="color: #999">......</span>
          </span>
        </p>
      </div>
      <div>
        <el-divider></el-divider>
        <p style="color: #999;">请使用USB连接手机</p>
      </div>
    </div>
    <div style="width: 40%" class="layout-column__center">
      <img src="../assets/images/phone.png" width="70%">
    </div>
  </div>
</template>

<script>
export default {
  name: "NoDevice",
  methods: {
    refresh() {
      this.$emit("getDevice");
    }
  }
};
</script>

<style>
.no-devices {
  padding: 50px 24px;
  width: 100%;
  height: 100%;
}
</style>


