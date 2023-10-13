import tkinter

CELLSIZE = 48   #1マスのピクセル数

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

#座標の移動（座標、ベクトル番号）
def moveposition(pos, vectol):
    x = pos[0] + vectable[vectol][0]
    y = pos[1] + vectable[vectol][1]
    return (x,y)

#四角形の描画（座標、色）
def drawrect(pos, color):
    xa = pos[0] * CELLSIZE
    ya = pos[1] * CELLSIZE
    xb = xa + CELLSIZE
    yb = ya + CELLSIZE
    canvas.create_rectangle(xa, ya, xb, yb, fill=color, width=2)


root = tkinter.Tk()
root.geometry("528x528")
canvas = tkinter.Canvas(root, width=528, height=528)

canvas.pack()

startpos = (5,5)#開始位置

drawrect(startpos, 'red')#開始地点に四角形を描画

for vec in range(8):#8方向に移動
    temppos = startpos
    for i in range(4):
        temppos = moveposition(temppos, vec)
        drawrect(temppos, 'Cyan')#移動先に四角形を描画

root.mainloop()


