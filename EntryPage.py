import os
from tkinter import *
import tkinter as tk
from AnnotationPage import AnnotationPage
from Detection import Detect
class EntryPage:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.master.geometry("700x220")
        self.master.title('Automatic Annotation')
        canvas= Canvas(self.master)
        canvas.place()
        back_color="#3b3561"
        text_color="#d1d1d1"
        button_color="#dd7373"
        frame_top=Frame(self.master, bg=back_color)
        frame_top.place(relx=0.01,rely=0.01,relwidth=0.98,relheight=0.98)
        
        frame_1=Frame(frame_top,bg=back_color)
        frame_1.place(relx=0.01,rely=0.01,relwidth=0.75,relheight=0.2375)
        label_ckpt=Label(frame_1, text='Ckpt name:',font='Verdana 8 bold',bg=back_color,fg=text_color)
        label_ckpt.pack(padx=10,pady=10,side=LEFT)
        
        textbox_ckpt=Text(frame_1,height=1.2,width=35)
        textbox_ckpt.pack(side=RIGHT)
        
        frame_2=Frame(frame_top,bg=back_color)
        frame_2.place(relx=0.01,rely=0.2575,relwidth=0.75,relheight=0.2375)
        label_anno=Label(frame_2, text='Label Map folder:',font='Verdana 8 bold',bg=back_color,fg=text_color)
        label_anno.pack(padx=10,pady=10,side=LEFT)
        
        textbox_anno=Text(frame_2,height=1.2,width=35)
        textbox_anno.pack(side=RIGHT)
        
        frame_3=Frame(frame_top,bg=back_color)
        frame_3.place(relx=0.01,rely=0.5075,relwidth=0.75,relheight=0.2375)
        label_model=Label(frame_3, text='Model folder:',font='Verdana 8 bold',bg=back_color,fg=text_color)
        label_model.pack(padx=10,pady=10,side=LEFT)
        
        textbox_model=Text(frame_3,height=1.2,width=35)
        textbox_model.pack(side=RIGHT)
        
        frame_4=Frame(frame_top,bg=back_color)
        frame_4.place(relx=0.01,rely=0.7525,relwidth=0.75,relheight=0.2375)
        label_image=Label(frame_4, text='Image folder:',font='Verdana 8 bold',bg=back_color,fg=text_color)
        label_image.pack(padx=10,pady=10,side=LEFT)
        
        textbox_image=Text(frame_4,height=1.2,width=35)
        textbox_image.pack(side=RIGHT)
        
        def start_annotation():
            detect=Detect()
            ckpt=textbox_ckpt.get("1.0",END).split('\n')[0]
            model=textbox_model.get("1.0",END).split('\n')[0]
            image=textbox_image.get("1.0",END).split('\n')[0]
            anno=textbox_anno.get("1.0",END).split('\n')[0]
            if ckpt=='':
                self.new_window('','','','',[],[])
            else:
                detected_objects_list=[]
                detected_objects_list=detect.annotate(model,anno,image,ckpt)
                category_index=detect.category_index_return()
                self.new_window(ckpt,anno,model,image,detected_objects_list,category_index)
        
        button_start=Button(frame_top,text="Start Annotation",command=start_annotation,bg=button_color,fg=text_color)
        button_start.pack(anchor=E,padx=10,pady=50)
        
    def new_window(self,ckpt,anno,model,image,detected_objects_list,category_index):
        self.newWindow = tk.Toplevel(self.master)
        self.app = AnnotationPage(self.newWindow,ckpt,anno,model,image,detected_objects_list,category_index)