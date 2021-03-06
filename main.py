# Author:
# _____ ___
#|  ___/ _ \__/\__
#| |_ | | | \    /
#|  _|| |_| /_  _\
#|_|   \___/  \/


from tkinter import *
from tkinter import filedialog
from pathlib import Path
import requests


class Tester:
    def __init__(self):
        # CREATE WINDOW
        self.root = Tk()
        self.root.title("WEB FINDER - find dead websites")

        self.import_button = Button(self.root, text="Import", anchor="n", command=lambda:self.browse_files())
        self.import_button.grid(row=2, column=2)
        self.source = ""
        self.import_label = Label(self.root, text="Select a file to import", anchor="s")
        self.import_label.grid(row=1, column=2)

        self.test_button = Button(self.root, height=5, width=45, text="Test links", command=lambda:self.process_and_test())
        self.test_button.grid(row=4, column=1)

        self.list_all = Listbox(self.root, width=50, height=50)
        self.list_all.grid(row=1, rowspan=4, column=0)
        self.list_all_label = Label(self.root, text="All links checked")
        self.list_all_label.grid(row=0, column=0)

        self.list_invalid = Listbox(self.root, width=50, height=45)
        self.list_invalid.grid(row=1, rowspan=3, column=1)
        self.list_invalid_label = Label(self.root, text="All invalid links")
        self.list_invalid_label.grid(row=0, column=1)

        self.export_button = Button(self.root, text="Export", anchor="n", command=lambda:self.save_file())
        self.export_button.grid(row=4, column=2)
        self.export = []
        self.export_label = Label(self.root, text="Export data", anchor="s")
        self.export_label.grid(row=3, column=2)

        self.root.mainloop()

    def browse_files(self):
        self.filename = filedialog.askopenfilename(initialdir = Path.home(),
                                              title = "Select a File",
                                              filetypes = (("Text files", "*.txt*"),
                                                           ("all files", "*.*")))
        self.source = self.filename
        self.import_label.configure(text="Source: "+self.filename)

    def save_file(self):
        self.files = [("Text files", "*.txt*"),
                      ("all files", "*.*")]
        self.file = filedialog.asksaveasfile(filetypes = self.files, defaultextension = self.files)
        print(self.file)
        for link in self.export:
            self.file.write(link+"\n")
        self.file.close()

    def process_and_test(self):
        if self.source:
            self.list_all.delete(0, self.list_all.size())
            self.list_invalid.delete(0, self.list_invalid.size())
            self.source_file = open(self.source, "r")
            self.all_index = 1
            self.invalid_index = 1
            for line in self.source_file:
                self.list_all.insert(self.all_index, line[:-1])
                try:
                    ret = requests.head(line[:-1])
                except:
                    print(line[:-1])
                    self.list_invalid.insert(self.invalid_index, line[:-1])
                    self.export.insert(len(self.export), line[:-1])
            self.source_file.close()
        else:
            self.test_button.configure(text="please select a file first")
