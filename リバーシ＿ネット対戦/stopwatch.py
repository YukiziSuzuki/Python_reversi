#ストップウォッチ
import tkinter
import threading

#タイマー処理（約一秒周期）
def timerctrl():
    global sec 
    sec += running
    #ウィジェット変数の値を変更
    textv.set("sec=" + str(sec))
    #タイマーを作成
    timer = threading.Timer(1, timerctrl)
    timer.start()   #タイマーを開始

    #ボタンが押されたときに実行する関数
def button_click(event):
    global sec, running 
    running ^= 1
    if running != 0:
        sec = 0    #秒カウンターをリセット
        textv.set("sec=" + str(sec))

#メインウィンドウを作成
root = tkinter.Tk()
sec = 0 #秒カウンター
running = 0 #実行中フラグ

#Labelウィジェットを作成
lab = tkinter.Label(root, text="Stop watch")
lab.place(x=20, y=70, width=160, height=20)

#文字列型のウィジェット変数を作成
textv = tkinter.StringVar()
#Entryウィジェットを作成
ent = tkinter.Entry(root, textvariable=textv)
ent.place(x=20, y=70, width=160, height=20)

#Buttonウィジェットを作成
btn = tkinter.Button(root, text="START/STOP")
btn.place(x=20, y=120, width=160, height=40)
#ボタンが押されたときに実行する関数を登録
btn.bind("<Button-1>", button_click)

#スレッドを作成
thread = threading.Thread(target=timerctrl)
thread.daemon = True
thread.start() #スレッドを開始

root.mainloop()

