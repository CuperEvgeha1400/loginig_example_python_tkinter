import tkinter as tk
from login_window import LoginWindow

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Логин')
    login_window = LoginWindow(root)
    root.mainloop()
