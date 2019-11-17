import axios from 'axios'
import router from '../router'
const baseURL = process.env.NODE_ENV === 'development' ? 'http://192.168.8.105:5000/' : 'http://0.0.0.0:5000/'
const service = axios.create({
  // baseURL: 'http://localhost:9080/'//辉哥
  baseURL: 'http://127.0.0.1:5000/'
})
console.log(1)
service.interceptors.request.use(
  config => {
    // if (store.state.token) {
    //   // 让每个请求携带自定义token 请根据实际情况自行修改
    //   config.headers['token'] = store.state.token
    // }
    return config
  },
  error => {
    console.log(error)
    Promise.reject(error)
  }
)

service.interceptors.response.use(
  response => {
    // const whiteList = ['/login', '/getSecurityCode', '/logout']
    // if (whiteList.some(n => response.config.url.includes(n))) {
    //   // if(response.config.url=="/excel-export-HSSF"){
    //   //   return response
    //   // }else{
    //     return response.data
    //   // }
    // }
    // const res = response.data
    // res.code = parseInt(res.code)
    // if (res.code !== 200) {
    //   // TODO: 确定状态码
    // }
    return response.data
  },
  error => {
    // const code = error.response.data.code
    // // 无权限，需要token
    // if (error.response.data.code === '000') {
    //   Message.error('token无效，请重新登录')
    //   router.push('/login')
    //   window.location.reload()
    //   store.dispatch('logout').then(() => {
    //     // window.location.href.includes('/login') ? window.location.reload() : router.push('/login')
    //   })
    // }
    return Promise.reject(error)
  }
)

export default service
