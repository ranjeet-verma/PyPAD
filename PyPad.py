import tkinter 
import os
import subprocess
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

import time

class PyPad:
    root = Tk()
    
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    #height = 400
    #width = 800
    
    root.attributes('-fullscreen', False)      #change it to True if you want the application to work in fullscreen mode
    
    TextArea = tkinter.Text(root, height = 25, width = 10, bg= "#FFFFFF", fg = "#0000ff")
    
    

    inp = tkinter.Text(root, height = 20, width = 70, bg = '#00ff55')
    empl = tkinter.Label(root, text = '', bg = 'black')
    emp1 = tkinter.Label(root, text = 'INPUT', bg = 'black', fg = 'white')
    emp2 = tkinter.Label(root, text = 'OUTPUT', bg = 'black', fg = 'white')
    
    output = tkinter.Text(root, height = 20, width = 70, bg = '#005588', fg = "#ffff00")
    
    
    MenuBar = Menu(root)
    File = Menu(MenuBar, tearoff =0)
    Edit = Menu(MenuBar, tearoff =0)
    Mode = Menu(MenuBar, tearoff =0)
    Help = Menu(MenuBar, tearoff =0)
    Execute = Menu(MenuBar, tearoff =0)
    Options = Menu(MenuBar, tearoff =0)
    
    
    ScrollBar = Scrollbar(TextArea)
    file = None
    
    
    
    def __init__(self, **kwargs):
        try:
            self.root.wm_iconbitmap("icon.ico")
        except:
            pass
        
        try:
            self.width = kwargs['width']
        except:
            pass
            
        try:
            self.height = kwargs['height']
        except:
            pass
            
        self.root.title("PYPAD")
        
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        left = (screenWidth/2 - self.width/2)
        top = (screenHeight/2 - self.height/2)
        
        self.root.geometry("%dx%d+%d+%d" % (self.width, self.height, left, top))
        
        self.root.grid_rowconfigure(0, weight =1)
        self.root.grid_columnconfigure(0, weight =1)
        
        self.TextArea.grid(row = 0, column = 0, sticky = N+E+S+W)
        self.inp.grid(row = 0, column = 1, sticky = N+E, pady = 20, padx = 20)
        
        self.output.grid(row = 0, column =1, sticky = E+S, pady = 20, padx = 20)
        self.empl.grid(row = 0, column = 1, sticky = W+E)
        self.emp1.grid(row = 0, column = 1, sticky = W+N+E)
        self.emp2.grid(row = 0, column = 1, sticky = W+S+E)
        
        
        self.File.add_command(label = "New", command = self.new)
        self.File.add_command(label = "Open", command  = self.openfile)
        self.File.add_command(label = "Save", command = self.save)
        self.File.add_command(label = "Save As", command = self.saveas)
        self.File.add_separator()
        self.File.add_command(label = "Exit", command = self.exitfile)
        
        self.MenuBar.add_cascade(label = "File", menu = self.File)
        
        self.Edit.add_command(label = "Cut", command = self.cut)
        self.Edit.add_command(label = "Copy", command = self.copy)
        self.Edit.add_command(label = "Paste", command = self.paste)
        
        self.MenuBar.add_cascade(label = "Edit", menu = self.Edit)
        
        self.Execute.add_command(label = "Python", command = self.exePython)
        self.Execute.add_command(label = "C++", command = self.exeCplusplus)
        self.Execute.add_command(label = "C", command = self.exeC)
        self.Execute.add_command(label = "Java", command = self.exeJava)
        
        self.MenuBar.add_cascade(label = "Run", menu = self.Execute)
        

        self.Options.add_command(label = "Get output in another window", command = self.window)
        self.MenuBar.add_cascade(label = "Options", menu = self.Options)
        
        self.Help.add_command(label = "About", command = self.about)
        self.MenuBar.add_cascade(label = "Help", menu = self.Help)
        
        self.root.config(menu = self.MenuBar)
        
        self.ScrollBar.pack(side = RIGHT, fill =Y)
        
        self.ScrollBar.config(command = self.TextArea.yview)
        self.TextArea.config(yscrollcommand = self.ScrollBar.set)
        self.output.configure(state = 'disabled')
        
    def takeinp(self):
        inp = self.inp.get('1.0', 'end-1c')
        return inp.encode('utf-8')
    
    def exitfile(self):
        if(self.file == None):
            ret = tkinter.messagebox.askokcancel("Hey!!", "Do you want to save the file?")
            if (ret ==1):
                self.save()
        self.root.destroy()
        
    def openfile(self):
        self.file = askopenfilename(defaultextension = ".py", filetypes = [("All files", "*.*"),("Text Documents", "*.txt")])
            
        if self.file == "":
            self.file = None
        else:
            self.root.title(os.path.abspath(self.file) + " -PYPAD")
            
            self.TextArea.delete(1.0, END)
           
            file = open(self.file, "r")
            
            self.TextArea.insert(1.0, file.read())
            
            file.close()
            
    def new(self):
        self.root.title("PYPAD")
        self.file = None
        self.TextArea.delete(1.0, END)
        
    def saveas(self):
            f = self.file
            
            self.file = asksaveasfilename( initialfile = "Untitled.py", filetypes = [("All files", "*.*"),("Text Documents", "*.txt")])
            if (self.file == "" and f == ""):
                self.file = None
            elif(self.file == ""):
                self.file = f
                self.root.title(os.path.basename(self.file) + "-PYPAD")
            else:
                file = open(self.file, "w")
                file.write(self.TextArea.get(1.0, END))
                file.close()
                self.root.title(os.path.basename(self.file) + "-PYPAD")   
                
            
            
    def save(self, ext = ""):
        if(ext == "" and self.file!=None):
            str = os.path.splitext(self.file)[1]
        if self.file == None:
            self.file = asksaveasfilename( initialfile = "Untitled.py", defaultextension = ext, filetypes = [("All files", "*.*"),("Text Documents", "*.txt")])
            if self.file =="":
                self.file = None
                
            else:
                file = open(self.file, "w")
                file.write(self.TextArea.get(1.0, END))
                file.close()
                self.root.title(os.path.basename(self.file) + "-PYPAD")
                
        else:
            if (os.path.splitext(self.file)[1] == ext or (ext == ".cpp" and os.path.splitext(self.file)[1] == ".c") or (ext == ".cpp" and os.path.splitext(self.file)[1] == ".cp")):
                file = open(self.file, "w")
                file.write(self.TextArea.get(1.0, END))
                file.close()
                self.root.title(os.path.basename(self.file) + "-PYPAD")
            else:
                
                tkinter.messagebox.showwarning("Warning", "Please execute the file with proper extension.")
                return 0
                
                
               
    def cut(self):
        self.TextArea.event_generate("<<Cut>>")
            
    def copy(self):
        self.TextArea.event_generate("<<Copy>>")
            
    def paste(self):
        self.TextArea.event_generate("<<Paste>>")
        
        
        
    def exePython(self):
    
        text = self.TextArea.get(1.0, END)
        #print(len(str(text)))
        
        if(len(str(text)) == 1):
            return tkinter.messagebox.showwarning("Warning", "Nothing to execute")
    
    
    
        if(self.save(".py")!=0):
            
            if (self.file == None):
                tkinter.messagebox.showwarning("Warning", "Save the file.")
            else:
                
                st = self.takeinp()
                
                cmd = "python \"" + os.path.abspath(self.file) + "\""
                
                #print(cmd)
                
                out = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                #out.stdin.write(st)
                o, e = out.communicate(st)
                self.output.configure(state = 'normal')
                self.output.delete('1.0', END)
                self.output.insert('1.0', e)
                self.output.insert('1.0', o)
                self.output.configure(state = 'disabled')
                

                

            
    def exeCplusplus(self):
    
        text = self.TextArea.get(1.0, END)
        #print(len(str(text)))
        
        if(len(str(text)) == 1):
            return tkinter.messagebox.showwarning("Warning", "Nothing to execute")
    
    
        
    
        if(self.save(".cpp")!=0):
            if (self.file == None):
                tkinter.messagebox.showwarning("Warning", "Save the file.")
            else:
                
                st = self.takeinp()
                print(st)
                cmd = "g++ -o main.exe \"" + os.path.abspath(self.file) + "\""
                
                #print(cmd)
                
                out = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                #out.stdin.write(st)
                o, e = out.communicate()
                

                
                if(e == b''):
                    cmd = "./main.exe"
                    out = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                    out.stdin.write(st)
                    o1, e1 = out.communicate()
                    self.output.configure(state = 'normal')
                    self.output.delete('1.0', END)
                    self.output.insert('1.0', e1)
                    self.output.insert('1.0', o1)
                    self.output.configure(state = 'disabled')
                    
                else:
                    self.output.configure(state = 'normal')
                    self.output.delete('1.0', END)
                    self.output.insert('1.0', e)
                    self.output.configure(state = 'disabled')
                
                
    def exeC(self):
    
        text = self.TextArea.get(1.0, END)
        #print(len(str(text)))
        
        if(len(str(text)) == 1):
            return tkinter.messagebox.showwarning("Warning", "Nothing to execute")
    
    
    
    
        if(self.save(".c")!=0):
            if (self.file == None):
                tkinter.messagebox.showwarning("Warning", "Save the file.")
            else:
                
                st = self.takeinp()
                print(st)
                cmd = "gcc -o main.exe \"" + os.path.abspath(self.file) + "\""
                
                #print(cmd)
                
                out = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                #out.stdin.write(st)
                o, e = out.communicate()
                

                #t.insert('1.0', e)
                #t.insert('1.0', o)
                
                if(e == b''):
                    cmd = "./main.exe"
                    out = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                    out.stdin.write(st)
                    o1, e1 = out.communicate()
                    self.output.configure(state = 'normal')
                    self.output.delete('1.0', END)
                    self.output.insert('1.0', e1)
                    self.output.insert('1.0', o1)
                    self.output.configure(state = 'disabled')
                    
                else:
                    self.output.configure(state = 'normal')
                    self.output.delete('1.0', END)
                    self.output.insert('1.0', e)
                    self.output.configure(state = 'disabled')
                
                
    def exeJava(self):
    
        text = self.TextArea.get(1.0, END)
        #print(len(str(text)))
        
        if(len(str(text)) == 1):
            return tkinter.messagebox.showwarning("Warning", "Nothing to execute")
        
        if(self.save(".java")!=0):
            if (self.file == None):
                tkinter.messagebox.showwarning("Warning", "Save the file.")
            else:
                st = self.takeinp()
                store_cur_dir = os.getcwd()
                print(store_cur_dir)
                
                p = os.path.abspath(self.file)
                par = os.path.dirname(self.file)
                os.chdir(par)
                
                cmd = "javac \"" + p + "\""
                print(cmd)
                
                #print(cmd)
                
                out = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                #out.stdin.write(st)
                o, e = out.communicate()

                #t.insert('1.0', e)
                #t.insert('1.0', o)
                
                if(e == b''):
                    
                    name_without_extension = os.path.relpath(self.file, start = os.curdir).strip(".java")
                    cmd = "java \"" + name_without_extension + "\""
                    print(cmd)
                    out = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                    out.stdin.write(st)
                    o1, e1 = out.communicate()
                    self.output.configure(state = 'normal')
                    self.output.delete('1.0', END)
                    self.output.insert('1.0', e1)
                    self.output.insert('1.0', o1)
                    self.output.configure(state = 'disabled')
                    
                else:
                    self.output.configure(state = 'normal')
                    self.output.delete('1.0', END)
                    self.output.insert('1.0', e)
                    self.output.configure(state = 'disabled')
                    
                print("java exe done")
                os.chdir(store_cur_dir)
                
                
                
        
    def createNewWindow(self):
        neww = tkinter.Toplevel(self.root)
        return neww
        
    def about(self):
        tkinter.messagebox.showinfo("About PYPAD", "This is an editor which works as an interface between your code and command prompt and facilitates execution of codes written in Python, Java and C++."
        " You can write your codes here and execute it without bothering about anything else. You can also open files with proper extension which are written in the mentiones programming languages."
        " You just need to have installed gcc( for C), g++ (for C++), Python(for Python) and JVM(for Java) in your system. Enjoy.")
        
            
            
    def run(self):
        self.root.mainloop()

    def window(self):
        out = self.output.get('1.0', 'end-1c') 
        if(out == ""):
            tkinter.messagebox.showwarning("Warning", "Execute the code first by clicking on the programming language option.")
        else:
            n = self.createNewWindow()
            try:
                n.wm_iconbitmap("icon.ico")
            except:
                pass
            t = Text(n)
            t.pack()
            t.insert('1.0', out)
            
        
        
if __name__== '__main__':
    pypad = PyPad()
    pypad.run()
    
            



        
        
