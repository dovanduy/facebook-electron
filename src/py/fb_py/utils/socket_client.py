#!/usr/bin/env
# -*- coding: utf-8 -*-
# @Time     :2019/10/12 0012 10:20
# @Author   :lyh
# @Desc     : socket 客户端
import websocket
from websocket import create_connection
import utils.global_Param as gp

gp.init()
ws = None
try:
    import thread
except ImportError:
    import _thread as thread
import time



def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send(gp.get_value('send_msg'))

    """def run(*args):

        time.sleep(1)
    thread.start_new_thread(run, ())"""

def send_long_msg(msg):
    gp.set_value('send_msg', msg)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.3.5:9001/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    # ping_interval心跳发送间隔时间
    # ping_timeout 设置，发送ping到收到pong的超时时间
    ws.run_forever(ping_interval=60, ping_timeout=5)

def send_short_msg(msg):
    ws = create_connection('ws://192.168.3.5:9001/')
    ws.send(msg)
    #ws.recv()
    ws.close()
