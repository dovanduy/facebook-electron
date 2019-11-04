import service from './axios.js'

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

