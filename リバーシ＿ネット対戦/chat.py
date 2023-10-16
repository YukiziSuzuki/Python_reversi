import tkinter
import socket
import threading

PORTNUM = 8000 #ポート番号

#タイマー処理(約一秒周期)
def timerctrl():
    try:
        #UDP受信
        recvdata, fromdata = sock.recvfrom(16)
        #受信データを変換
        recvtext = str(recvdata, "utf-8")
        #送信元IPアドレスを表示
        ipaddr.set(fromdata[0])
    except socket.timeout: #受信タイムアウト
        recvtext = " "

    #データを受信した場合
    if recvtext != "":
        rxdata.set(recvtext)


    #タイマーを作成
    timer = threading.Timer(1, timerctrl)
    timer.start() #タイマーを開始


#ボタンが押されたときに実行する関数
def button_click(event):
    addr = ipaddr.get() #送信先IPアドレス
    data = txdata.get() #送信データ
    #UDP送信
    sock.sendto(bytes(data, "utf-8"), (addr, PORTNUM))

root = tkinter.Tk() #メインウィンドウを作成
root.geometry("320x240") #メインウィンドウのサイズを変更

#Labelウィジェットを作成
lab = tkinter.Label(root, text = "相手のIPアドレス")
lab.place(x=10, y=20, width=120, height=20)

#ウィジェット変数を作成
ipaddr = tkinter.StringVar()
ipaddr.set("192.168.x.x")  #IPアドレスを格納

#Entryウィジェットを作成
entl = tkinter.Entry(root, textvariable=ipaddr)
entl.place(x=120, y=20, width=120, height=20)

#Buttonウィジェットを作成
btn = tkinter.Button(root, text="送信")
btn.place(x=180, y=100, width=120, height=40)
#ボタンが押されたときに実行する関数を登録
btn.bind("<Button-1>", button_click)

#ウィジェット変数
rxdata = tkinter.StringVar()
rxdata.set("receive data") #送信データを格納
#エントリーを作成
ent3 = tkinter.Entry(root, textvariable=rxdata)
ent3.place(x=10, y=160, width=160, height=20)

#ネットワークを初期化
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("",PORTNUM))
sock.settimeout(0.1) #受信タイムアウトを設定

#スレッドを作成
thread = threading.Thread(target=timerctrl)
thread.daemon = True
thread.start() #スレッドを開始

root.mainloop()







