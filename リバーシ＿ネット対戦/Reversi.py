import tkinter

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

board = bytearray(BOARDW * BOARDW) #盤を管理する配列

playtbl = ["黒", "白"] #プレイヤーの表示名
colortbl = ["Black", "White"] #駒の色の配列
vectable = [
    (0,-1), #0:上
    (1,-1), #1:右上
    (1,0),  #2:右
    (1,1),  #3:右下
    (0,1),  #4:下
    (-1,1), #5:左下
    (-1,0), #6:左
    (-1,-1) #7:左上
]

#盤に書き込み（座標、駒の種類）
def setpiece(pos, num):
    index = (pos[1] * BOARDW) + pos[0]
    board[index] = num

#盤から読み込み（座標）
def getpiece(pos):
    index = (pos[1] * BOARDW) + pos[0]
    return board[index]

#盤の初期化
def initboard():
    global turn, passcnt, endflag
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
        nextrun()       #プレイヤー切り替え＆ゲームの判定
        redraw()        #再描画
        return
    
    x = int((event.x - OFSX) / CELLSIZE) #クリックされた場所の座標を計算
    y = int((event.y - OFSY) / CELLSIZE) #クリックされた場所の座標を計算
    pos = (x,y)
    if isinside(pos) == False: 
        return    #盤の外なら無効
    if turnablepiece(pos, turn) == 0: 
        return  #駒を置けない場合は無効
    for vectol in range(8): #石を反転
        loopcount = search(pos, vectol, turn)  #探索
        temppos = pos
        for i in range(loopcount):
            temppos = moveposition(temppos, vectol)   #座標を移動
            setpiece(temppos, turn)   #駒を置き換える

    setpiece(pos, turn) #自分の駒を置く
    nextturn()          #手番を変更
    redraw()            #再描画


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
#メインウィンドウのキャンバスを作成
canvas = tkinter.Canvas(root, width=576, height=480)
canvas.pack()                     #メインウィンドウのキャンバスを配置

#クリックイベントが発生した時に実行する関数を登録
canvas.bind("<Button-1>", canvas_click)
initboard()                       #盤の初期化
root.mainloop()                   #メインループ




