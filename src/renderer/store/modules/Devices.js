import {
  getDevices
} from '@/api/index.js'

const state = {
  devices: []
}

const mutations = {
  SET_DEVICES(state, devices) {
    state.devices = devices
  }
}

const actions = {
  getDevicesList({
    commit
  }) {
    return new Promise((resolve, reject) => {
      getDevices().then(res => {
        if (res.success) {
          let data = res.data
          let devices = []
          for (let key in data) {
            data[key].jwd = ''
            data[key].location = ''
            devices.push(data[key])
          }
          commit('SET_DEVICES', devices)
          setTimeout(() => {
            devices.forEach(item => {
              let webview = document.getElementById('web' + item.device_id)
              // webview.insertCSS("html,body{margin:0;}canvas{border:none!important;transform:scale(0.71111);transform-origin: left top;position:absolute;left:0;top:0}")
              webview.insertCSS("html,body{margin:0;}canvas{border:none!important;transform:scale(0.53333);transform-origin: left top;position:absolute;left:0;top:0}")
            })
          }, 1000)
          resolve()
        } else {
          commit('SET_DEVICES', [])
          reject()
        }
      }).catch(e => {
        commit('SET_DEVICES', [])
        reject()
      })
    })
  }
}

export default {
  state,
  mutations,
  actions
}