<template>
  <div id="app">
    <div class="drag-header" style="-webkit-app-region: drag;"></div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'electron-vue',
  data () {
    return {
      scoket: null
    }
  },
  mounted () {
    let self = this
  },
  beforeDestroy () {
    // this.scoket.close()
  }
}
</script>

<style>
  /* CSS */
  .drag-header{
    position: absolute;
    top:0;
    left: 0;
    width: 100%;
    height: 24px;
  }
  #app{
    height: 100vh;

  }
</style>
