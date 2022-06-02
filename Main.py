import tkinter as tk
from EntryPage import EntryPage
def main(): 
    root = tk.Tk()
    root.iconbitmap('ic_launcher.ico')
    app = EntryPage(root)
    root.mainloop()

if __name__ == '__main__':
    main()