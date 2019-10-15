const ws = require('nodejs-websocket')
const { ipcMain, BrowserWindow } = require('electron')
const hostname = '192.168.3.5'
const port = '9001'

const createServer = function () {
  ws.createServer(function (conn) {
    console.log('Server running at ws://%s:%d/', hostname, port);
      conn.on("text", function(data) {
          console.log("Received:" + data);
          try {
            // let data = JSON.parse(data)
            BrowserWindow.webContents.send('socketMsg', data)
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
          console.log(err);
      });
  }).listen(port)
}


module.exports = createServer