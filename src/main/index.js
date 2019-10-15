import { app, BrowserWindow, Menu, MenuItem, ipcMain } from 'electron'
const ws = require('nodejs-websocket')
const path = require('path')
/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = require('path').join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow
const winURL = process.env.NODE_ENV === 'development'
  ? `http://localhost:9080`
  : `file://${__dirname}/index.html`

function createWindow () {
  /**
   * Initial window options
   */
  mainWindow = new BrowserWindow({
    frame: false,
    titleBarStyle: 'hidden',
    height: 780,
    useContentSize: true,
    icon: path.join(__dirname, '../renderer/assets/images/logo.png'),
    width: 1120,
    webPreferences: {
      webSecurity: false,
      plugins: true
    }
  })

  mainWindow.loadURL(winURL)

  
  const hostname = '192.168.3.5'
  const port = '9001'

  const createServer = function () {
    ws.createServer(function (conn) {
      console.log('Server running at ws://%s:%d/', hostname, port);
        conn.on("text", function(data) {
            console.log("Received:" + data);
            try {
              // let data = JSON.parse(data)
              mainWindow.webContents.send('socketMsg', data)
            } catch (e) {
              console.log(e)
            }
            // conn.sendText(data.toUpperCase() + "!!!");
        });
        conn.on("close", function(code, reason) {
            console.log("Connection closed");
        });
        conn.on("error", function(err) {
            console.log("handle err");
        });
    }).listen(port)
  }
  createServer()
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})

// 设备右键菜单
ipcMain.on('showDeviceRightMenu', (event, arg) => {
  const menu = new Menu()
  menu.append(new MenuItem({label: '设备账号信息', click: function () {
    event.sender.send('rightMenuEvent', 'get_detail');
  }}))
  menu.append(new MenuItem({label: '添加定时任务', click: function () {
    event.sender.send('rightMenuEvent', 'add_task');
  }}))
  menu.append(new MenuItem({label: '添加好友', click: function () {
    event.sender.send('rightMenuEvent', 'add_friends');
  }}))
  menu.append(new MenuItem({label: '添加小组', click: function () {
    event.sender.send('rightMenuEvent', 'add_group');
  }}))
  menu.append(new MenuItem({label: '锁屏', click: function () {
    event.sender.send('rightMenuEvent', 'lock');
  }}))
  menu.append(new MenuItem({label: '解屏', click: function () {
    event.sender.send('rightMenuEvent', 'unlock');
  }}))
  const win = BrowserWindow.fromWebContents(event.sender)
  menu.popup(win)
})



