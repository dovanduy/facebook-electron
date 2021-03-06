import service from './axios.js'
// console.log
export const getDevices = () => {
  return service.get(`/find_PhoneInfo`)
}

export const lockScreen = (id) => {
  return service.post(`/lock`, JSON.stringify({ device_id: id }))
}

export const unlockScreen = (id) => {
  return service.post(`/unlock`, JSON.stringify({ device_id: id }))
}

export const chooseMethod = (data) => {
  return service.post(`/choose_method`, JSON.stringify(data))
}

export const updateDevice = (data) => {
  return service.post(`/updateDevice`, JSON.stringify(data))
}

export const login = (data) => {
  return service.post(`/login`, JSON.stringify(data))
}
//注册
export const register = (data) => {
  return service.post(`/reg`, JSON.stringify(data))
}

export const setLocation = (data) => {
  return service.post(`/update_location_services`, JSON.stringify(data))
}
//messager设置好友通过发送信息
export const userPassSend = (msg) => {
  return service.get(`/sendMsg?msg=${msg}`)
}
//messager群发消息
export const massText = (data) => {
  return service.post(`/update_location_services`, JSON.stringify(data))
}
//获取分组
export const getTeam = (account) => {
  return service.get(`/findTeam?account=${account}`)
}
//获取全部账号
export const getAllAcount = (account) => {
  return service.get(`/findEmp?account=${account}`)
}
//添加分组
export const addTeam = (params) => {
  return service.post(`/addTeam`, params)
}
//删除分组
export const delTeam = (id) => {
  return service.get(`/removeTeam?id=${id}`)
}
//删除人员
export const delUser = (id) => {
  return service.get(`/removeUser?id=${id}`)
}
//设置分组
export const setGroup = (params) => {
  return service.post(`/empGroup`, params)
}
//------------------养号-------------------
//养号类型
export const findHaveNoType = () => {
  return service.get(`/findHaveNoType`)
}
//查询养号
export const aKeyHaveNo = (params) => {
  return service.post(`/aKeyHaveNo`, params)   //参数：user_id:用户id，type_id 操作类型id
}


