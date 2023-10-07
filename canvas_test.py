import tkinter

root = tkinter.Tk()
root.geometry("600x480")
canvas = tkinter.Canvas(root, width=600, height=480)    #Canvasウィジットを作成
canvas.pack()                                           #Canvasウィジットを配置

FONTSIZE = ("",24)                                      #フォントサイズを指定

#四角形を描写
canvas.create_rectangle(50, 150, 150, 250, fill="red")

#円を描写
canvas.create_oval(250, 150, 350, 250, fill="blue")

#テキストを描画
msg = "ABCDEFG"
canvas.create_text(500, 200, text=msg, font=FONTSIZE)

root.mainloop()