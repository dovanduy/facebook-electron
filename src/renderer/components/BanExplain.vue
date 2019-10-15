<template>
<el-drawer
  title="避免封号建议"
  :visible.sync="show"
  size="400px"
  :before-close="handleClose">
  <div style="padding: 20px;margin-top: -32px">
    <el-divider content-position="left">个人账号被封原因：</el-divider>
    <p>1.IP地址: 尽量避免IP切换过于频繁、切换地域跨度太大。</p>
    <p>2.账号: 尽量避免注册信息不实(身份、头像、名称、联系方式等)</p>
    <p>3.登录: 尽量避免同个IP或设备多次注册、同时登录、同设备多账号、同账号多设备、频繁登退等。</p>
    <p>4.运营: 尽量避免长时间不登录、无更新、短时间内大量操作(加好友/加小组/群发/拉人入群等)</p>
    <p>5.其他: 尽量避免被投诉</p>
    <el-divider content-position="left">Facebook粉丝主页被封原因：</el-divider>
    <p>1.侵权：使用没有版权和许可的音乐及图像商标等。</p>
    <p>2.内容：烟酒、赌、或与成人相关内容且对访客年龄等不设限。</p>
    <p>3.过度转发：原创内容不多，过度转发。</p>
    <p>4.欺诈：宣传内容与实质促销不符</p>
  </div>
</el-drawer>
</template>

<script>
export default {
  name: 'BanExplain',
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
    }
  },
  methods: {
    handleClose () {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
p{
  margin-bottom: 10px;
  color: #666;
}
</style>

