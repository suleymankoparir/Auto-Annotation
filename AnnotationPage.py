import os
from AnnotationTool import AnnotationTool
import numpy as np
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image


    
class AnnotationPage:
    def __init__(self, master,ckpt,anno,model,image,detected_objects_list,category_index):
        self.master = master
        self.master.geometry("700x500")
        self.master.title('Automatic Annotation')
        canvas= Canvas(self.master)
        canvas.place()       
        
        annotationTool=AnnotationTool()
        
        
        frame_left=Frame(self.master, bg='#add8e6')
        frame_left.place(relx=0.01,rely=0.0,relwidth=0.28,relheight=0.99)
        
        frame_right=Frame(self.master, bg='#add8e6')
        frame_right.place(relx=0.30,rely=0.0,relwidth=0.69,relheight=0.99)
        
        selected_image=0
        imageLabel = Label(frame_right)
        def change_image(index):
            if index==-1:
                w, h = 320, 320
                data = np.zeros((h, w, 3), dtype=np.uint8)
                img=ImageTk.PhotoImage(Image.fromarray(data))
            else:
                img = ImageTk.PhotoImage(Image.fromarray(detected_objects_list[index][0]['image']))
            global selected_image
            selected_image=index
            #imageLabel = Label(frame_right,image=img)
            imageLabel.configure(image=img)
            imageLabel.image = img
            imageLabel.pack(expand=1)
        
        
        dropbox_option=StringVar(frame_left)
        dropbox_option.set("\t")
        dropbox_menu=OptionMenu(
            frame_left,
            dropbox_option,
            'null'
        )
        if len(category_index)>0:
            dropbox_option.set("")
            dropbox_menu['menu'].delete(0,'end')
            for i in range(1,len(category_index)+1):
                name=category_index[i]['name']
                dropbox_menu['menu'].add_command(label=name, command=tk._setit(dropbox_option, name))
        if len(detected_objects_list)>0:
            change_image(0)
        else:
            change_image(-1)
            
        dropbox_menu.pack(padx=10,pady=10,side=TOP)
        def change_fn():
            annotationTool.changeAnnotationFile(dropbox_option.get().split('\n')[0] ,detected_objects_list[selected_image][0]['name'], detected_objects_list[selected_image][0]['filepath'])
            return
        button_change=Button(frame_left,text="Change label",command=change_fn)
        button_change.pack(anchor=S)
        
        def delete_fn():
            global selected_image
            filename=detected_objects_list[selected_image][0]['name'].split('.')[0]
            if os.path.exists(image+filename+'.jpg'):
                os.remove(image+filename+'.jpg')
            if os.path.exists(image+filename+'.xml'):
                os.remove(image+filename+'.xml')
            detected_objects_list.remove(detected_objects_list[selected_image])
            if len(detected_objects_list)==1:
                change_image(0)
            else:
                selected_image-=1
                right_fn()
        button_delete=Button(frame_left,text="Delete",command=delete_fn)
        button_delete.pack(anchor=S,pady=10)
        
        frame_left_bottom=Frame(frame_left,bg='#add8e6')
        frame_left_bottom.place(relx=0.2,rely=0.8,relwidth=0.6,relheight=0.19)
        
        def left_fn():
            global selected_image
            if len(detected_objects_list)==0:
                change_image(-1)
            elif(selected_image!=0):
                selected_image-=1
                change_image(selected_image)
                
        def right_fn():
            global selected_image
            if len(detected_objects_list)==0:
                change_image(-1)
            elif(selected_image!=len(detected_objects_list)-1):
                selected_image+=1
                change_image(selected_image)
                
        button_left=Button(frame_left_bottom,text="<",command=left_fn)
        button_left.pack(padx=10,pady=10,side=LEFT)
        
        button_right=Button(frame_left_bottom,text=">",command=right_fn)
        button_right.pack(padx=10,pady=10,side=RIGHT)
    def close_windows(self):
        self.master.destroy()