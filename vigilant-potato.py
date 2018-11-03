
import tkinter as tk
import wordclipper

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Vigilant-Potato')
    app1 = wordclipper.WordClipper(master=root)
    app1.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
    root.mainloop()