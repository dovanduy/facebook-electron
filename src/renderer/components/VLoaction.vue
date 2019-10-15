<template>
<div class="location layout-column">
  <el-card class="layout-column" header="请点击地图拾取经纬度坐标后，将经纬度复制到设备列表中点击确定" style="height:65%">
    <webview
      src="https://api.map.baidu.com/lbsapi/getpoint/index.html"
      style="width:100%;height:100%"
    >
    </webview>
  </el-card>
  <el-card class="devices-list layout-column" header="设备列表">
    <el-table :data="devices" size="mini" style="height:100%" class="layout-column">
      <el-table-column prop="device_remark" label="设备" width="120"></el-table-column>
      <el-table-column prop="device_model" label="型号" width="120"></el-table-column>
      <el-table-column prop="fb_nickName" label="FB账号" width="120"></el-table-column>
      <el-table-column prop="jwd" label="经纬度">
        <template slot-scope="scope">
          <el-input size="mini" v-model="scope.row.jwd"></el-input>
        </template>
      </el-table-column>
      <el-table-column prop="location" label="地址">
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="primary"
            @click="setLoaction(scope.row)">保存</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="resetLoaction(scope.row)">重置</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</div>
</template>

<script>
export default {
  name: 'VLoaction',
  data () {
    return {
      geoc: new BMap.Geocoder()
    }
  },
  computed: {
    devices () {
      let res = JSON.parse(JSON.stringify(this.$store.state.Devices.devices))
      return res
    } 
  },
  mounted () {
  },
  methods: {
    setLoaction (row) {
      let ll = row.jwd.split(',')
      let point = new BMap.Point(Number(ll[0]), Number(ll[1]))
      this.getLocation(point).then(res => {
        console.log(res)
        row.location = res.province + ' ' + res.city + ' ' + res.district + ' ' + res.street
      })
    },
    resetLocation () {

    },
    getLocation (point) {
      return new Promise((resolve, reject) => {
        let self = this
        this.geoc.getLocation(point, function (rs) {
          let addComp = rs.addressComponents;
          resolve({
            province: addComp.province,
            city: addComp.city,
            district: addComp.district,
            street: addComp.street
          })
        })
      })
    }
  }
}
</script>

<style lang="scss">
.location{
  height: 100%;
  position: relative;
  z-index: 3;
  .el-card__body{
    flex: 1;
  }
  .devices-list{
    margin: 20px 0;
    width: 100%;
    flex: 1;
  }
}
</style>

