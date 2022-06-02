import tkinter as tk # this is in python 3.4. For python 2.x import Tkinter
from PIL import Image, ImageTk

class RectangleManagement():
    def __init__(self,canvas):
        self.x = self.y = 0
        
        self.rect = None

        self.start_x = None
        self.start_y = None
        self.item_counter=-1
        self.selected_rect=None
        self.selected_index=0
        self.title="Null"
        self.canvas=canvas
        
        self.x1=0
        self.y1=0
        self.x2=100
        self.y2=100
        
        global Rect
        Rect=[]
        
        global images
        images=[]
    
    def item_tag(self):
        self.item_counter+=1
        return str(self.item_counter)+'_rectangle'
    def latest_tag(self):
        return str(self.item_counter)+'_rectangle'
    def rect_list_return_unmapped(self,ratio):
        temp_list=[]
        for rect in Rect:
            rect_info={
                'xmin':int((rect['xmin']-self.x1)/ratio),
                'ymin':int((rect['ymin']-self.y1)/ratio),
                'xmax':int((rect['xmax']-self.x1)/ratio),
                'ymax':int((rect['ymax']-self.y1)/ratio),
                'title':rect['title']
                }
            temp_list.append(rect_info)
        return temp_list
            
    def rect_coord_mapped(self,xmin,ymin,xmax,ymax,ratio):
        xmin=int(xmin*ratio)+self.x1
        ymin=int(ymin*ratio)+self.y1
        xmax=int(xmax*ratio)+self.x1
        ymax=int(ymax*ratio)+self.y1
        coord={
            'xmin':xmin,
            'ymin':ymin,
            'xmax':xmax,
            'ymax':ymax           
            }
        return coord
        
    def change_title(self):
        if self.selected_rect!=None:
            if self.title!='Null':
                self.canvas.itemconfigure(self.selected_rect['tag']+'_txt',text=self.title)
                self.canvas.delete(self.selected_rect['tag']+'_txt_back')
                text_item=self.canvas.find_withtag(self.selected_rect['tag']+'_txt')
                bbox=self.canvas.bbox(text_item)
                rect_item = self.canvas.create_rectangle(bbox, outline="black", fill="black",tag=self.selected_rect['tag']+'_txt_back')
                self.canvas.tag_raise(text_item,rect_item)   
                self.selected_rect['title']=self.title
    def transparent_im(self,xmin,ymin,xmax,ymax,alpha,fill):
        alpha=int(alpha*255)
        fill=self.canvas.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (xmax-xmin, ymax-ymin), fill)
        images.append(ImageTk.PhotoImage(image))
        self.canvas.create_image(xmin, ymin, image=images[-1], anchor='nw',tag=self.latest_tag()+'_im')
    def on_button_press(self, event):
        if event.x>=self.x1 and event.x<=self.x2 and event.y>=self.y1 and event.y<=self.y2:
            self.start_x = event.x
            self.start_y = event.y
        
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1,tag=self.item_tag(),width=5)
        else:
            self.start_x=-1
            self.start_y=-1
    def on_move_press(self, event):
        if self.start_x!=-1 and self.start_y!=-1:
            self.curX, self.curY = (event.x, event.y)
            
            self.curX=self.x2 if self.curX>self.x2 else self.curX
            self.curX=self.x1 if self.curX<self.x1 else self.curX
            
            self.curY=self.y2 if self.curY>self.y2 else self.curY
            self.curY=self.y1 if self.curY<self.y1 else self.curY
            
            self.canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)
    def delete_all(self):
        self.selected_rect=None
        for item in Rect:
            self.canvas.delete(item['tag'])
            self.canvas.delete(item['tag']+'_im')
            self.canvas.delete(item['tag']+'_txt')
            self.canvas.delete(item['tag']+'_txt_back')
        Rect.clear()
            
    def delete(self):
        if  self.selected_rect!= None:
            self.canvas.delete(self.selected_rect['tag'])
            self.canvas.delete(self.selected_rect['tag']+'_im')
            self.canvas.delete(self.selected_rect['tag']+'_txt')
            self.canvas.delete(self.selected_rect['tag']+'_txt_back')
            Rect.remove(self.selected_rect)
            self.selected_rect=None       
        else:
            print('selected rect is null')
    def drawRect(self,xmin,ymin,xmax,ymax,alpha,fill,title):
        self.Rect=self.canvas.create_rectangle(xmin, ymin, xmax, ymax,tag=self.item_tag(),width=5)
        text_item=self.canvas.create_text(xmin, ymin-10,text=title,anchor='w',fill='white',font=('Helvetica 12 bold'),tag=self.latest_tag()+'_txt')
        bbox=self.canvas.bbox(text_item)
        rect_item = self.canvas.create_rectangle(bbox, outline="black", fill="black",tag=self.latest_tag()+'_txt_back')
        self.canvas.tag_raise(text_item,rect_item)
        rect_info={
            'xmin':xmin,
            'ymin':ymin,
            'xmax':xmax,
            'ymax':ymax,
            'tag':self.latest_tag(),
            'title':title
            }
        Rect.append(rect_info)
        self.canvas.tag_bind(self.latest_tag(),'<Double-1>',self.DoubleClick)
        self.canvas.tag_bind(self.latest_tag()+'_im','<Double-1>',self.DoubleClick)
        self.transparent_im(xmin, ymin, xmax, ymax, alpha, fill)
        self.rect=None
        
    def DoubleClick(self,event):
        x=event.x
        y=event.y
        counter=0
        for item in Rect:
            xmin=item['xmin']
            ymin=item['ymin']
            xmax=item['xmax']
            ymax=item['ymax']
            if x>=xmin and x<=xmax and y>=ymin and y<=ymax:
                if self.selected_rect != None:
                    self.canvas.itemconfig(self.selected_rect['tag'],outline="black")
                self.selected_rect=item
                self.selected_index=counter
                self.canvas.itemconfig(item['tag'],outline="#fb0")
                break
            counter=counter+1
            
            
    def on_button_release(self, event):
        if self.start_x!=-1 and self.start_y!=-1:
            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            xmin=ymin=xmax=ymax=0
            if self.start_x<self.curX:
                xmin=self.start_x
                xmax=self.curX
            else:
                xmin=self.curX
                xmax=self.start_x
            if self.start_y<self.curY:
                ymin=self.start_y
                ymax=self.curY
            else:
                ymin=self.curY
                ymax=self.start_y
            rect_info={
                'xmin':xmin,
                'ymin':ymin,
                'xmax':xmax,
                'ymax':ymax,
                'tag':self.latest_tag(),
                'title':self.title
                }
                
            text_item=self.canvas.create_text(xmin, ymin-10,text=self.title,anchor='w',fill='white',font=('Helvetica 12 bold'),tag=self.latest_tag()+'_txt')
            bbox=self.canvas.bbox(text_item)
            rect_item = self.canvas.create_rectangle(bbox, outline="black", fill="black",tag=self.latest_tag()+'_txt_back')
            self.canvas.tag_raise(text_item,rect_item)
            Rect.append(rect_info)
            self.canvas.tag_bind(self.latest_tag(),'<Double-1>',self.DoubleClick)
            self.canvas.tag_bind(self.latest_tag()+'_im','<Double-1>',self.DoubleClick)
            self.transparent_im(xmin, ymin, xmax, ymax, .4, 'blue')
            self.rect=None
        pass
    def bind(self):
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release) 