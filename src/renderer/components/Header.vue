<template>
<div class="header layout-row">
  <div class="logo layout-row">
    <span class="logo-img iconfont icon-facebook"></span>
    <p class="layout-column logo-title">
      <span style="font-size:16px">FaceBook 群控系统</span>
      <span style="color: #999;margin-top: 5px;font-size:14px">FB Group Control System</span>
    </p>
  </div>
  <el-tabs class="menu flex" v-model="activeTab">
    <el-tab-pane name="status">
      <span slot="label" class="tab-title">
        <i class="iconfont icon-liaotian"></i>
        <span>状态</span>
      </span>
    </el-tab-pane>
    <el-tab-pane name="group">
      <span slot="label">
        <i class="iconfont icon-jiaqun"></i>
        <span>好友/小组</span>
      </span>
    </el-tab-pane>
    <el-tab-pane name="groupSend">
      <span slot="label">
        <i class="iconfont icon-qunfa"></i>
        <span>群发</span>
      </span>
    </el-tab-pane>
    <el-tab-pane name="post">
      <span slot="label">
        <i class="iconfont icon-tiezi"></i>
        <span>发帖</span>
      </span>
    </el-tab-pane>
    <el-tab-pane name="sys">
      <span slot="label">
        <i class="iconfont icon-shezhi"></i>
        <span>系统设置</span>
      </span>
    </el-tab-pane>
  </el-tabs>
  <div class="user layout-row">
    <el-avatar style="align-self:center" size="small" icon="el-icon-user-solid"></el-avatar>
    <el-dropdown style="align-self:center;margin-left: 10px;cursor:pointer">
      <span class="el-dropdown-link">
        测试账号<i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>修改密码</el-dropdown-item>
        <el-dropdown-item>个人信息</el-dropdown-item>
        <el-dropdown-item>退出</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</div>
</template>

<script>
export default {
  name: 'Header',
  data () {
    return {
      activeTab: 'status'
    }
  },
  watch: {
    activeTab: {
      handler: function (val) {
        switch (val) {
          case 'status':
            this.$router.push('/home/status')
            break
          case 'group':
            this.$router.push('/home/group')
            break
        }
      },
      immediate: true
    }
  }
}
</script>

<style>
.menu{
  margin-left: 40px;
}
.tab-title{
  font-size: 16px;
}
.el-tabs__nav-wrap::after{
  display: none;
}
.header{
  height: 60px;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.logo-img{
  align-self: center;
  margin-right: 10px;
  font-size: 34px;
  color: #3a5998;
}

.logo-title{
  align-self: center;
}
</style>

