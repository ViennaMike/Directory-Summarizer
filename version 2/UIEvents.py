# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:30:25 2015

@author: mike
"""

from Tkinter import *
from tkFileDialog import askdirectory, askopenfilenames, asksaveasfilename    
import ttk
import tkMessageBox
import file_digester as fd

def sumDirectory():
    summary.sum_type='directory'
    for child in frame1.winfo_children(): child.configure(state='disable')
    summary.start = askdirectory(title="Choose top level directory", mustexist=True) 
    for child in frame1.winfo_children(): child.configure(state='disable')
    for child in frame2.winfo_children(): child.configure(state='normal')
    
def sumFiles():
    summary.sum_type='files'
    for child in frame1.winfo_children(): child.configure(state='disable')
    more = True
    summary.fileList = []
    while more:   
      tempFileList = list(askopenfilenames(parent=root,title='Choose a file'))
      summary.fileList.extend(tempFileList)
      more = tkMessageBox.askyesno(message='Do you want to select additional files?', icon='question', title='More?')  
    for child in frame2.winfo_children(): child.configure(state='normal')
     
def getDestination():
    for child in frame2.winfo_children(): child.configure(state='disable')
    summary.dest = asksaveasfilename(parent=root,title='Select file to store summary')
    for child in frame3.winfo_children(): child.configure(state='normal')
    
def runSummary():
#    root.withdraw()
    for child in frame3.winfo_children(): child.configure(state='disable')
    fd.main(summary.sum_type, summary.start, summary.fileList, summary.dest, summary.len)
    if tkMessageBox.showinfo(message='Finished', type="ok"):
        root.destroy()

class summaryClass:
    def __init__(self):
        self.start = ''
        self.dest = ''
        self.len = '5'
        self.fileList = []

summary = summaryClass()
try: 
    root = Tk()
    # root.withdraw()
    root.title("Summarize Files")
    frame1 = ttk.Labelframe(root, padding="2 3 12 12", text='Select Source')
    frame1.grid(column=0, row=0, sticky=(N, W, E, S))
    frame1.columnconfigure(0, weight=1)
    frame1.rowconfigure(0, weight=1)	
    button1 = ttk.Button(frame1, text="Directory Contents", command=sumDirectory).grid(column=0, row=0, sticky=W)
    button2 = ttk.Button(frame1, text="Selected Files", command=sumFiles).grid(column=2, row=0, sticky=W)
    for child in frame1.winfo_children(): child.grid_configure(padx=5, pady=5)
    
    frame2 = ttk.LabelFrame(root, padding="2 3 12 12", text='Run Summarizer')
    frame2.grid(column=0, row=1, sticky=(N, W, E, S))
    frame2.columnconfigure(0, weight=1)
    frame2.rowconfigure(0, weight=1)	
    ttk.Label(frame2, text='Number of sentences in each summary:').grid(column=0, row=1, sticky=(W, E))
    sentences = IntVar()
    length = ttk.Entry(frame2, textvariable=sentences).grid(column=1, row=1, sticky=W)
    sentences.set(5)
    button3 = ttk.Button(frame2, text="Select Destination", command=getDestination).grid(column=0, row=2, sticky=W)
    for child in frame2.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        child.configure(state='disable')
        
    frame3 = ttk.LabelFrame(root, padding="2 3 12 12", text='Run Summarizer')
    frame3.grid(column=0, row=2, sticky=(N, W, E, S))
    frame3.columnconfigure(0, weight=1)
    frame3.rowconfigure(0, weight=1)	
    button4 = ttk.Button(frame3, text="Run", command=runSummary).grid(column=2, row=2, sticky=W)
    for child in frame3.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        child.configure(state='disable')  
        
    root.mainloop() 

except:
    root.destroy()
    sys.exit() 