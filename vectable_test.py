import tkinter

CELLSIZE = 48

vectable = [
    (0,-1),
    (1,-1),
    (1,0),
    (1,1),
    (0,1),
    (-1,1),
    (-1,0),
    (-1,-1),
]

def moveposition(pos, vectol):
    x = pos[0] + vectable[vectol][0]
    y = pos[1] + vectable[vectol][1]
    return (x,y)

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

startpos = (5,5)

drawrect(startpos, 'red')

for vec in range(8):
    temppos = startpos
    for i in range(4):
        temppos = moveposition(temppos, vec)
        drawrect(temppos, 'Cyan')

root.mainloop()


