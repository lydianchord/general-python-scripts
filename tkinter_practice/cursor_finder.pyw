import tkinter as tk
from tkinter import ttk

root = tk.Tk()
l = ttk.Label(root,
              text='Press space to find and copy \nthe current mouse position.')
l.grid()


def get_mouse(event):
    pos = '%d, %d' % (event.x_root, event.y_root)
    l['text'] = pos
    root.clipboard_clear()
    root.clipboard_append(pos)


root.bind('<space>', get_mouse)

root.mainloop()
