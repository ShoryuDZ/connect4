from tkinter import *

def begin_game():
    print("No func here yet...")

window = Tk()
window.geometry("500x500")
window.title("Connect4 Player")

frame = Frame(window)
frame.pack()

slogan = Button(frame, text="Start", command=begin_game)
slogan.pack(side=LEFT)

window.mainloop()