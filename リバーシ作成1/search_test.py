import tkinter

CELLSIZE = 48       #1マスのピクセル数
FONTSIZE = ("", 24) #フォントサイズの設定
BOARDW = 8          #盤面の横幅
OFSX = 2*CELLSIZE   #盤のオフセットx座標
OFSY = 1*CELLSIZE   #盤のオフセットy座標
TYPE_NONE = 255     #駒の種類：なし
TYPE_BLACK = 0      #駒の種類：黒
TYPE_WHITE = 1      #駒の種類：白

#盤を管理する配列
board = bytearray(BOARDW * BOARDW)

colortbl = ["Black", "White"]#駒の色の配列

vectable = [#ベクトルテーブル
    (0,-1),#0:上
    (1,-1),#1:右上
    (1,0),#2:右
    (1,1),#3:右下
    (0,1),#4:下
    (-1,1),#5:左下
    (-1,0),#6:左
    (-1,-1),#7:左上
]

#盤に書き込み（座標、駒の種類）
def setpiece(pos,num):
    index = (pos[1] * BOARDW) + pos[0]
    board[index] = num

#盤から読み込み（座標）
def getpiece(pos):
    index = (pos[1] * BOARDW) + pos[0]
    return board[index]

#座標の移動（座標、ベクトル番号）
def moveposition(pos, vectol):
    x = pos[0] + vectable[vectol][0]
    y = pos[1] + vectable[vectol][1]
    return (x,y)


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

#駒/盤を描画（座標、駒の種類）
def drawpiece(pos,num):
    xa = pos[0] * CELLSIZE + OFSX
    ya = pos[1] * CELLSIZE + OFSY
    xb = xa + CELLSIZE
    yb = ya + CELLSIZE
    canvas.create_rectangle(xa, ya, xb, yb, fill="green", width=2)
    if num == TYPE_NONE: return   #numが255ならdrawpieceを終了
    d = int(CELLSIZE/10)
    canvas.create_oval(xa+d, ya+d, xb-d, yb-d, fill=colortbl[num], width=0)   #numが0なら黒、1なら白を描く




root = tkinter.Tk()
root.geometry("576x480")
canvas = tkinter.Canvas(root, width=576, height=480)  
canvas.pack()

for y in range(BOARDW):
    for x in range(BOARDW):
        setpiece((x,y), TYPE_NONE)  #初期盤面を作成

setpiece((3,3), TYPE_BLACK) #初期配置
setpiece((4,3), TYPE_WHITE) #初期配置
setpiece((5,3), TYPE_WHITE) #初期配置
setpiece((6,3), TYPE_BLACK) #初期配置

for y in range(BOARDW):
    for x in range(BOARDW):
        drawpiece((x,y), getpiece((x,y)))   #駒を表示

piece = search((3,3), 2, TYPE_BLACK) #右方向に探索
msg = "Rssult:" + str(piece)
canvas.create_text(288, 456, text = msg, font = FONTSIZE)

root.mainloop()


