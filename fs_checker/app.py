import tkinter as tk
from tkinter import ttk
import threading

class InputDialog:
    def __init__(self):
        self.result = None
        self.root = None
        self.create_window()

    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Ввод текста")

        window_width = 300
        window_height = 100
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        self.entry = ttk.Entry(frame)
        self.entry.pack(fill=tk.X, pady=(0, 10))
        self.entry.focus()

        submit_button = ttk.Button(frame, text="Отправить", command=self.on_submit)
        submit_button.pack()

        self.root.bind('<Return>', lambda event: self.on_submit())

    def on_submit(self):
        self.result = self.entry.get()
        self.root.quit()
        self.root.destroy()

    def get_input(self):
        #thread = threading.Thread(target=self.create_window)
        #thread.start()
        self.root.mainloop()
        return self.result

def get_user_input():
    dialog = InputDialog()
    return dialog.get_input().split()
