import tkinter

CELLSIZE = 48

#クリックイベントが発生した時に実行する関数
def canvas_click(event):
    xa = event.x
    ya = event.y
    xv = xa + CELLSIZE
    yb = ya + CELLSIZE
    #クリックされた場所に四角形と円を描画
    canvas.create_rectangle(xa, ya, xv, yb, fill="green", width=2)
    d = int(CELLSIZE/10)
    canvas.create_oval(xa+d, ya+d, xv-d, yb-d, fill="white", width=2)

root = tkinter.Tk()
root.geometry("640x480")
canvas = tkinter.Canvas(root, width=640, height=480)

canvas.pack()


#クリックイベントが発生した時に実行する関数を設定
canvas.bind("<Button-1>", canvas_click)

root.mainloop()
