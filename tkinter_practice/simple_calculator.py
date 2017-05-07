import tkinter as tk
from tkinter import ttk


class Calculator:
    
    def __init__(self, master):
        master.title('Calculator')
        self.frame = frame = ttk.Frame(master)
        
        self.total = 0
        self.entered_number = 0
        
        self.total_label_text = tk.IntVar()
        self.total_label_text.set(self.total)
        self.total_label = ttk.Label(frame, textvariable=self.total_label_text)
        
        self.label = ttk.Label(frame, text='Total:')
        
        vcmd = frame.register(self.validate)
        self.entry = ttk.Entry(frame, validate='key', validatecommand=(vcmd, '%P'))
        
        self.add_button = ttk.Button(frame, text='+', command=lambda: self.update('add'))
        self.subtract_button = ttk.Button(frame, text='-', command=lambda: self.update('subtract'))
        self.reset_button = ttk.Button(frame, text='Reset', command=lambda: self.update('reset'))
        
        # --Layout--
        
        default_pad = 5
        
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        
        frame.grid(padx=10, pady=10, sticky='nsew')
        
        self.label.grid(row=0, column=0, sticky='nw')
        self.total_label.grid(row=0, column=1, columnspan=2, sticky='ne')
        
        self.entry.grid(row=1, column=0, columnspan=3, sticky='ew')
        
        self.add_button.grid(row=2, column=0)
        self.subtract_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2)
        
        num_cols, num_rows = frame.grid_size()
        for i in range(num_cols):
            frame.grid_columnconfigure(i, weight=1, pad=default_pad)
        for i in range(num_rows):
            frame.grid_rowconfigure(i, weight=1, pad=default_pad)
    
    def validate(self, new_text):
        if not new_text:
            self.entered_number = 0
            return True
        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False
    
    def update(self, method):
        if method == 'add':
            self.total += self.entered_number
        elif method == 'subtract':
            self.total -= self.entered_number
        elif method == 'reset':
            self.total = 0
        
        self.total_label_text.set(self.total)
        self.entry.delete(0, 'end')


if __name__ == '__main__':
    root = tk.Tk()
    gui = Calculator(root)
    root.mainloop()
