import os
from AnnotationTool import AnnotationTool
from RectangleManagement import RectangleManagement
import numpy as np
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image

    
class AnnotationPage:
    def __init__(self, master,ckpt,anno,model,image,detected_objects_list,category_index):
        self.master = master
        self.master.title('Automatic Annotation')    
        self.master.iconbitmap('ic_launcher.ico')
        self.canvas = tk.Canvas(self.master, width=1000, height=750)
        self.canvas.pack(side="top", fill="both", expand=False)
        self.master.resizable(width=False, height=False)
        
        back_color="#3b3561"
        text_color="#d1d1d1"
        button_color="#dd7373"
        self.canvas.configure(bg=back_color)
        annotationTool=AnnotationTool()
        rectangleManagement=RectangleManagement(self.canvas)
        
        rectangleManagement.x1=0
        rectangleManagement.x2=700
        
        rectangleManagement.y1=0
        rectangleManagement.y2=500
        
        frame_left=Frame(self.master, bg=back_color)
        frame_left.place(relx=0.01,rely=0.1,relwidth=0.28,relheight=0.80)
        
        selected_image=0
        imageLabel = Label(self.master)
        def deleteRect(self):
            if rectangleManagement.selected_rect!=None:
                global selected_image
                if len(detected_objects_list[selected_image])!=1:
                    detected_objects=detected_objects_list[selected_image][rectangleManagement.selected_index]
                    detected_objects_list[selected_image].remove(detected_objects)
                    rectangleManagement.delete()
                else:
                    detected_objects_list[selected_image][0]['title']=''
                    detected_objects_list[selected_image][0]['xmin']=0
                    detected_objects_list[selected_image][0]['ymin']=0
                    detected_objects_list[selected_image][0]['xmax']=0
                    detected_objects_list[selected_image][0]['ymax']=0
                    rectangleManagement.delete()
        def drawAnnotations(index,ratio):
            rects=detected_objects_list[index]
            for rect in rects:
                if rect['title']!='':
                    drawing_coords=rectangleManagement.rect_coord_mapped(rect['xmin'], rect['ymin'], rect['xmax'], rect['ymax'], ratio)
                    rectangleManagement.drawRect(
                        drawing_coords['xmin'], 
                        drawing_coords['ymin'], 
                        drawing_coords['xmax'], 
                        drawing_coords['ymax'], 
                        .2, 
                        'blue', 
                        rect['title']
                        )
        def dropbox_changed(*args):
            global selected_image
            if rectangleManagement.selected_rect!=None:
                if len(detected_objects_list[selected_image])>rectangleManagement.selected_index:
                    detected_objects_list[selected_image][rectangleManagement.selected_index]['title']=dropbox_option.get()
                
                rectangleManagement.title=dropbox_option.get()
                rectangleManagement.change_title()
                filename=detected_objects_list[selected_image][0]['name'].split('.')[0]
                if os.path.exists(image+filename+'.xml'):
                    annotationTool.changeAnnotationTitle(dropbox_option.get().split('\n')[0] ,detected_objects_list[selected_image][0]['name'], detected_objects_list[selected_image][0]['filepath'],rectangleManagement.selected_index)
        def change_image(index):
            rectangleManagement.delete_all()
            if index==-1:
                w, h = 640, 640
                data = np.zeros((h, w, 3), dtype=np.uint8)
                img=Image.fromarray(data)
            else:
                img=Image.fromarray(detected_objects_list[index][0]['image'])
            if(img.width>=img.height):
                self.ratio=640/img.width
            else:
                self.ratio=640/img.height
            img_new_w=int(img.width*self.ratio)
            img_new_h=int(img.height*self.ratio)
            img=img.resize((img_new_w,img_new_h))
            img=ImageTk.PhotoImage(img)
            
            global selected_image
            selected_image=index
            im_x=650
            im_y=370
            c_im=self.image=self.canvas.create_image(im_x,im_y, image=img)
            self.canvas.image=img


            
            rectangleManagement.x1=im_x-int(img_new_w/2)
            rectangleManagement.x2=im_x+int(img_new_w/2)
            
            rectangleManagement.y1=im_y-int(img_new_h/2)
            rectangleManagement.y2=im_y+int(img_new_h/2)
            if (index!=-1):
                drawAnnotations(index, self.ratio)
            
        
        dropbox_option=StringVar(frame_left)
        dropbox_option.set("\t")
        
        dropbox_menu=OptionMenu(
            frame_left,
            dropbox_option,
            'null'
        )
        dropbox_menu.config(width=15)
        dropbox_menu.config(bg=button_color,fg=text_color)
        dropbox_menu['menu'].config(bg=button_color,fg=text_color)
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
        dropbox_option.trace('w', dropbox_changed)
        
        self.master.bind("<Delete>",deleteRect)
        
        def draw_rect():
            rectangleManagement.bind()
        button_draw=Button(frame_left,text="Draw",command=draw_rect,width=20,fg=text_color,bg=button_color)
        button_draw.pack(anchor=S)
        
        def delete_fn():
            rectangleManagement.delete_all()
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
        button_delete=Button(frame_left,text="Delete Image",command=delete_fn,width=20,fg=text_color,bg=button_color)
        button_delete.pack(anchor=S,pady=10)
        
        frame_left_bottom=Frame(frame_left,bg=back_color)
        frame_left_bottom.place(relx=0.2,rely=0.3,relwidth=0.6,relheight=0.19)
        def write_annotation():
           global selected_image
           detected_objects=detected_objects_list[selected_image]
           if detected_objects[0]['title']!='':
               annotationTool.createAnnotationFile(
                   detected_objects[0]['width'],
                   detected_objects[0]['height'],
                   detected_objects[0]['xmin'],
                   detected_objects[0]['ymin'],
                   detected_objects[0]['xmax'],
                   detected_objects[0]['ymax'],
                   detected_objects[0]['title'],
                   detected_objects[0]['name'],
                   detected_objects[0]['filepath']
                   )
               if len(detected_objects)>1:
                   for i in range(1,len(detected_objects)):
                       annotationTool.addObject(
                           detected_objects[i]['xmin'], 
                           detected_objects[i]['ymin'],
                           detected_objects[i]['xmax'], 
                           detected_objects[i]['ymax'], 
                           detected_objects[i]['title'], 
                           detected_objects[0]['name'],
                           detected_objects[0]['filepath']
                           )
           else:
               filename=detected_objects_list[selected_image][0]['name'].split('.')[0]
               if os.path.exists(image+filename+'.xml'):
                   os.remove(image+filename+'.xml')
        def update_detected_objects():
            global selected_image
            detected_objects=detected_objects_list[selected_image]
            width=detected_objects[0]['width']
            height=detected_objects[0]['height']
            name=detected_objects[0]['name']
            filepath=detected_objects[0]['filepath']
            image=detected_objects[0]['image']
            new_rects=rectangleManagement.rect_list_return_unmapped(self.ratio)
            detected_objects.clear()
            for rect in new_rects:
                temp={
                    'width':width,
                    'height':height,
                    'xmin':rect['xmin'],
                    'ymin':rect['ymin'],
                    'xmax':rect['xmax'],
                    'ymax':rect['ymax'],
                    'title':rect['title'],
                    'name':name,
                    'filepath':filepath,
                    'image':image
                    }
                detected_objects.append(temp)
            if len(detected_objects)==0:
                temp={
                    'width':width,
                    'height':height,
                    'xmin':0,
                    'ymin':0,
                    'xmax':0,
                    'ymax':0,
                    'title':'',
                    'name':name,
                    'filepath':filepath,
                    'image':image
                    }
                detected_objects.append(temp)
            write_annotation()
                    
                    
        
        def left_fn():
            global selected_image
            if len(detected_objects_list)==0:
                change_image(-1)
            elif(selected_image!=0):
                update_detected_objects()
                selected_image-=1
                change_image(selected_image)
                
                
        def right_fn():
            global selected_image
            if len(detected_objects_list)==0:
                change_image(-1)
            elif(selected_image!=len(detected_objects_list)-1):
                update_detected_objects()
                selected_image+=1
                change_image(selected_image)
                
                
        button_left=Button(frame_left_bottom,text="<",command=left_fn,fg=text_color,bg=button_color)
        button_left.pack(padx=10,pady=10,side=LEFT)
        
        button_right=Button(frame_left_bottom,text=">",command=right_fn,fg=text_color,bg=button_color)
        button_right.pack(padx=10,pady=10,side=RIGHT)
    
    def close_windows(self):
        self.master.destroy()