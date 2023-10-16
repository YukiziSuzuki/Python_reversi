import tkinter
import socket
import threading

PORTNUM = 8000     #ポート番号
CELLSIZE = 48      #1マスのピクセル数
FONTSIZE = ("", 24) #フォントサイズの設定
BOARDW = 8         #盤面の幅
OFSX = 2*CELLSIZE  #盤のオフセットx座標
OFSY = 1*CELLSIZE  #盤のオフセットy座標
TYPE_BLACK = 0     #駒の種類：黒
TYPE_WHITE = 1     #駒の種類：白
TYPE_NONE = 255    #駒の種類：なし
turn = TYPE_BLACK  #手番
passcnt = 0        #パスの回数
endflag = False    #終了フラグ
timelimit = 0      #制限時間


board = bytearray(BOARDW * BOARDW) #盤を管理する配列

playtbl = ["黒", "白"] #プレイヤーの表示名
colortbl = ["Black", "White"] #駒の色の配列
vectable = [#8方向のベクトルテーブル
    (0,-1), #0:上
    (1,-1), #1:右上
    (1,0),  #2:右
    (1,1),  #3:右下
    (0,1),  #4:下
    (-1,1), #5:左下
    (-1,0), #6:左
    (-1,-1) #7:左上
]

#手番の表示名
whotbl = ["(あなた)", "(相手)"]

#タイマー処理（約一秒周期）
def timerctrl():
    global myturn, timelimit, endflag

    try:
        #UDP受信
        recvdata, fromdata = sock.recvfrom(16)
        #受信データを変換
        recvtext = str(recvdata, "utf-8")
        #相手のIPアドレス
        ipaddr.set(fromdata[0])

    except socket.timeout: #受信タイムアウト
        recvtext = " "
        if timelimit > 0:
            timelimit -= 1
            if timelimit <= 0: #制限時間切れの場合
                canvas.create_text(80, 20, text="Timeout", font=FONTSIZE)
                endflag = True  #ゲーム終了

    if recvtext == "OK":  #レスポンスを受信
        timelimit = 0      #制限時間をリセット
    elif recvtext != "":  #受信データがある場合
        sendsub("OK")      #レスポンスを送信
        if recvtext == "start":  #相手が接続要求
            myturn = TYPE_WHITE  #手番を白に設定
            initboard()          #盤の初期化
        elif recvtext =="pass":  #相手がパス
            #プレイヤー切り替え＆ゲームの判定
            nextturn()
            redraw()           #画面全体を再描画 
        else:                     #相手が駒を置いた場合
            pos = (int(recvtext[0:1]), int(recvtext[1:2]))
            confirmpiece(pos, turn)  #駒を確定

    timer = threading.Timer(1, timerctrl)
    timer.start() #タイマーを開始


#データを送信
def sendsub(sendtext):
    global timelimita
    addr = ipaddr.get()  #送信先IPアドレス
    #送信データ
    senddata = bytes (sendtext, "utf-8")
    #UDP送信
    sock.sendto(senddata, (addr, PORTNUM))
    if sendtext != "OK":
        timelimit = 5  #レスポンスの制限時間


#開始ボタンクリック時に実行する関数
def button_click(event):
    global myturn
    sendsub("start")    #接続要求を送信
    myturn = TYPE_BLACK #手番を黒に設定
    initboard()         #盤の初期化

    
#盤に書き込み（座標、駒の種類）
def setpiece(pos, num):
    index = (pos[1] * BOARDW) + pos[0]
    board[index] = num

#盤から読み込み（座標）
def getpiece(pos):
    index = (pos[1] * BOARDW) + pos[0]
    return board[index]

#接続画面を表示
def connection():
    canvas.place_forget() #キャンバスを非表示
    lab.place(x=130, y=150, width=120, height=20)
    ent.place(x=250, y=150, width=120, height=20)
    btn.place(x=220, y=210, width=120, height=60)


#盤の初期化
def initboard():
    global turn, passcnt, endflag

    lab.place_forget() #ラベルを非表示
    ent.place_forget() #エントリーを非表示
    btn.place_forget() #ボタンを非表示
    canvas.place(x=0, y=0) #キャンバスを表示

    for y in range(BOARDW):
        for x in range(BOARDW):
            setpiece((x,y), TYPE_NONE)

    setpiece((3,3), TYPE_BLACK)   #黒
    setpiece((4,4), TYPE_BLACK)   #黒
    setpiece((3,4), TYPE_WHITE)   #白
    setpiece((4,3), TYPE_WHITE)   #白
    turn = TYPE_BLACK             #手番
    passcnt = 0                   #パスの回数
    endflag = False               #終了フラグ
    redraw()                     #再描画


#クリックイベントが発生した時に実行する関数
def canvas_click(event):
    if endflag == True: #ゲーム終了
        initboard()     #盤の初期化
        return
    
    if passcnt > 0:     #パス
        nextturn()       #プレイヤー切り替え＆ゲームの判定
        redraw()        #再描画
        return
    
    x = int((event.x - OFSX) / CELLSIZE) #クリックされた場所の座標を計算
    y = int((event.y - OFSY) / CELLSIZE) #クリックされた場所の座標を計算
    pos = (x,y)
    if isinside(pos) == False: 
        return    #盤の外なら無効
    if turnablepiece(pos, turn) == 0: 
        return  #駒を置けない場合は無効
    
    #石の座標を送信
    sendsub(str(pos[0])+str(pos[1]))
    confirmpiece(pos, turn)  #駒を確定


#駒を確定（座標、駒の種類）
def confirmpiece(pos,turn):
    for vectol in range(8): #石を反転
        loopcount = search(pos, vectol, turn)  #探索
        temppos = pos
        for i in range(loopcount):
            temppos = moveposition(temppos, vectol)   #座標を移動
            setpiece(temppos, turn)    #駒を置き換える

    setpiece(pos, turn) #自分の駒を置く
    #プレイヤーの切り替え＆ゲームの判定
    nextturn()
    redraw()            #画面全体を再描画
    

#プレイヤー切り替え＆ゲームの判定
def nextturn():
    global passcnt, endflag, turn
    turn ^= 1        #手番を変更
    empty = 0        #空きマスの数
    for y in range(BOARDW):
        for x in range(BOARDW):
            if getpiece((x,y)) == TYPE_NONE:
                empty += 1
            if turnablepiece((x,y), turn) > 0:
                passcnt = 0
                return
            
    if empty == 0:    #空きマスがない場合は終了
        endflag = True
        return
    
    passcnt += 1      #パスが発生
    if passcnt >= 2:  #連続パスの場合はゲーム終了
        endflag = True


#座標の移動（座標、ベクトル番号）
def moveposition(pos, vectol):
    x = pos[0] + vectable[vectol][0]
    y = pos[1] + vectable[vectol][1]
    return (x,y)

#反転できる駒の数を取得（座標、駒の種類）   
def turnablepiece(pos, num):
    if getpiece(pos) != TYPE_NONE: 
        return 0 #既に駒がある場合は無効
    total = 0
    for vectol in range(8): #8方向に探索
        total += search(pos, vectol, num)
    return total
        
#探索（座標、ベクトルテーブルの番号、駒の種類）
def search(pos, vectol, num):
    piece = 0  #駒の数
    while True:
        pos = moveposition(pos, vectol)
        if isinside(pos) == False:
            return 0 #盤の外へ出た場合は無効
        if getpiece(pos) == TYPE_NONE:
            return 0 #数えられない場合は無効
        if getpiece(pos) == num:
            break  #目的の駒を検出した場合は終了
        piece += 1 #駒の数をカウント
    return piece

#指定座標の範囲をチェック（座標）
def isinside(pos):
    if pos[0]<0 or pos[0]>=8: return False  #範囲外
    if pos[1]<0 or pos[1]>=8: return False  #範囲外
    return True #範囲内

#駒・盤を表示（座標、駒の種類）
def drawpiece(pos, num):
    xa = pos[0] * CELLSIZE + OFSX
    ya = pos[1] * CELLSIZE + OFSY
    xb = xa + CELLSIZE
    yb = ya + CELLSIZE
    canvas.create_rectangle(xa, ya, xb, yb, fill="Green", width=2)

    if num == TYPE_NONE: return
    d = int(CELLSIZE/10)
    canvas.create_oval(xa+d, ya+d, xb-d, yb-d, fill=colortbl[num], width=2)


#画面全体を再描画
def redraw():
    canvas.create_rectangle(0, 0, 576, 480, fill="Khaki1")

    black = 0 #黒の数
    white = 0 #白の数
    for y in range(BOARDW):
        for x in range(BOARDW):
            pos = (x,y)
            num = getpiece(pos)
            if num == TYPE_BLACK: black += 1
            if num == TYPE_WHITE: white += 1
            drawpiece(pos, num) #盤・駒を描画
            #assist(pos, turn)  #アシスト機能

    msg = "黒" + str(black) + "　対　白" + str(white)
    canvas.create_text(288, 456, text=msg, font=FONTSIZE)
    msg = playtbl[turn] + "の番です"
    if passcnt > 0:        #パス
        msg += "(パス！　)"
    if endflag == True:    #ゲーム終了
        msg = "ゲーム終了！　"

    canvas.create_text(288, 24, text=msg, font=FONTSIZE)

#アシスト機能（座標、駒の種類）
def assist(pos, num2):
    piece = turnablepiece(pos, num2)    #反転できる駒の数を取得
    if piece == 0: return               #反転できる駒がない場合は無効
    x = pos[0] * CELLSIZE + OFSX + int(CELLSIZE/2) #駒の中心x座標
    y = pos[1] * CELLSIZE + OFSY + int(CELLSIZE/2) #駒の中心y座標
    canvas.create_text(x, y, text=str(piece), font=FONTSIZE, fill="yellow")


#メインプログラム
root = tkinter.Tk()               #メインウィンドウを作成
root.title("オセロ")              #メインウィンドウのタイトルを変更
root.geometry("576x480")          #メインウィンドウのサイズを変更

#Labelウィジェットを作成
lab = tkinter.Label(root, text = "相手のIPアドレス")

#ウィジェット変数を作成
ipaddr = tkinter.StringVar()
ipaddr.set("192.168.x.x")  #IPアドレスを格納

#Entryウィジェットを作成
ent = tkinter.Entry(root, textvariable=ipaddr)

#Buttonウィジェットを作成
btn = tkinter.Button(root, text="開始")
btn.bind("<Button-1>", button_click)

#メインウィンドウのキャンバスを作成
canvas = tkinter.Canvas(root, width=576, height=480)

#クリックイベントが発生した時に実行する関数を登録
canvas.bind("<Button-1>", canvas_click)
connection()                      #接続画面を表示

#ネットワークを初期化
sock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORTNUM))
#スレッドを作成
thread = threading.Thread(target = timerctrl)
thread.daemon = True
thread.start() #スレッドを開始

root.mainloop()                   #メインループ




