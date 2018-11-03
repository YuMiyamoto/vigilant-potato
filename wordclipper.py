#python3.6.6

import pyperclip
import os
import csv
import tkinter.simpledialog
import tkinter as tk
import webbrowser

class WordClipper(tk.LabelFrame):
    def __init__(self, master=None):
        super().__init__(master, text='WordClipper')
        self.show_widgets()
    
    def show_widgets(self):
        self.get_word_list()
        self.widget_list = []

        #create clip buttons
        for pass_name in self.word_list:
            if pass_name[2] == 'nolink':
                bgcolor = 'lightyellow'
            else:
                bgcolor = 'lightblue'
            self.new_button(pass_name[0], 15, bgcolor, self.word_clip)

        #create_new button
        self.new_button("create new", 15, "snow", self.create_new)

        #delete check button
        self.var = tkinter.IntVar()
        self.new_check_button("delete clip", self.var)

        #change pass button
        self.var_p = tkinter.IntVar()
        self.new_check_button("change pass", self.var_p)

        #change order
        self.var_o = tkinter.IntVar()
        self.new_check_button("change order", self.var_o)

    def new_button(self, text, width, bg, bind):
        b = tk.Button(self, text=text, width=width, bg=bg)
        b.bind("<ButtonRelease-1>", bind)
        b.pack()
        self.widget_list.append(b)

    def new_check_button(self, text, var):
        check = tk.Checkbutton(self, text=text, variable=var)
        check.pack(anchor=tk.W, padx=5)
        self.widget_list.append(check)

    def word_clip(self, event):
        if self.var.get() == 1:
            self.delete_button(event.widget["text"])
        elif self.var_p.get() == 1:
            self.change_clipword(event.widget["text"])
        elif self.var_o.get() == 1:
            self.change_order(event.widget["text"])
        else:
            for pass_name in self.word_list:
                try:
                    pass_name[0].index(event.widget["text"])
                    break
                except:
                    pass
            pyperclip.copy(pass_name[1])
            self.open_link(pass_name[2])

    def get_word_list(self):
        listfile = os.path.join(os.getcwd(), 'word_list.csv')
        self.word_list = []
        if os.path.exists(listfile):
            open_file = open(listfile)
            file_reader = csv.reader(open_file)
            for row in file_reader:
                self.word_list.append([row[0], row[1], row[2]])

    def create_new(self, event):
        #input title, word, link
        title = tkinter.simpledialog.askstring('input title', 'please input title')
        if(title == None or title == ''):
            return
        word = tkinter.simpledialog.askstring('input clipword', 'please input clipword')
        if(word == None or word == ''):
            return
        link = tkinter.simpledialog.askstring('input URL', 'please input URL')
        if(link == None or link == ''):
            link = 'nolink'
        
        #save title, word, link to csv file
        listfile = os.path.join(os.getcwd(), 'word_list.csv')
        open_file = open(listfile, 'a', newline='')
        output_writer = csv.writer(open_file)
        output_writer.writerow([title, word, link])
        open_file.close()
        
        self.reset_widgets()

    def delete_button(self, clipword):
        listfile = os.path.join(os.getcwd(), 'word_list.csv')
        self.word_list = []
        if os.path.exists(listfile):
            open_file = open(listfile)
            file_reader = csv.reader(open_file)
            for row in file_reader:
                if row[0] == clipword:
                    continue
                self.word_list.append([row[0], row[1], row[2]])

            open_file = open(listfile, 'w', newline='')
            output_writer = csv.writer(open_file)
            for d in self.word_list:
                output_writer.writerow(d)
            open_file.close()

            self.reset_widgets()

    def reset_widgets(self):
        for d in self.widget_list:
            d.destroy()
        self.show_widgets()
    
    def open_link(self, link):
        if link == 'nolink':
            return
        else:
            webbrowser.open(link)
    
    def change_clipword(self, button_name):
        word = tkinter.simpledialog.askstring('input clipword', 'please input clipword')
        if word:
            for w in self.word_list:
                if button_name == w[0]:
                    w[1] = word
            self.var_p.set(0)
            self.save_word_list()
            self.reset_widgets()

    def change_order(self, button_name):
        for a in self.word_list:
            if a[0] == button_name:
                break
        self.word_list.remove(a)
        self.word_list = [a] + self.word_list
        self.save_word_list()
        self.reset_widgets()

    def save_word_list(self):
        listfile = os.path.join(os.getcwd(), 'word_list.csv')
        open_file = open(listfile, 'w', newline='')
        output_writer = csv.writer(open_file)
        for d in self.word_list:
            output_writer.writerow(d)
        open_file.close()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Automate the Tiring Manual task')
    app1 = WordClipper(master=root)
    app1.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
    root.mainloop()