import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2 
import AnnotationTool
from AnnotationTool import AnnotationTool
import numpy as np
from matplotlib import pyplot as plt
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
annotationTool=AnnotationTool()
category_index=[]
def annotate(MODEL_PATH,ANNONATION_FOLDER_PATH,IMAGE_FOLDER_PATH,CHECKPOINT_NAME):
    LABEL_MAP_NAME = 'label_map.pbtxt'
    files = {
        'PIPELINE_CONFIG':os.path.join(MODEL_PATH, 'pipeline.config'),
        'LABELMAP': os.path.join(ANNONATION_FOLDER_PATH, LABEL_MAP_NAME)
    }
    configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)

    # Restore checkpoint
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(os.path.join(MODEL_PATH, CHECKPOINT_NAME)).expect_partial()

    @tf.function
    def detect_fn(image):
        image, shapes = detection_model.preprocess(image)
        prediction_dict = detection_model.predict(image, shapes)
        detections = detection_model.postprocess(prediction_dict, shapes)
        return detections
    global category_index
    category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])
    def auto_annotate(filepath,item):
        img = cv2.imread(filepath+item)
        height, width, _ = img.shape
        image_np = np.array(img)
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections

        # detection_classes should be ints.
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
                    image_np_with_detections,
                    detections['detection_boxes'],
                    detections['detection_classes']+label_id_offset,
                    detections['detection_scores'],
                    category_index,
                    use_normalized_coordinates=True,
                    max_boxes_to_draw=1,
                    min_score_thresh=.8,
                    agnostic_mode=False)
        detected_objects=[]
        for i in range (0,100):
            if(detections['detection_scores'][i]>.8):
                detected_object_name=category_index[detections['detection_classes'][i]+label_id_offset]['name']
                detected_object_ymin=detections['detection_boxes'][i][0]*height
                detected_object_xmin=detections['detection_boxes'][i][1]*width
                detected_object_ymax=detections['detection_boxes'][i][2]*height
                detected_object_xmax=detections['detection_boxes'][i][3]*width
                detected_object={
                    'title':detected_object_name,
                    'xmin':detected_object_xmin,
                    'ymin':detected_object_ymin,
                    'xmax':detected_object_xmax,
                    'ymax':detected_object_ymax,
                    'width':width,
                    'height':height,
                    'image':cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB),
                    'filepath':filepath,
                    'name':item
                    }
                detected_objects.append(detected_object)
        if len(detected_objects)==0:
                detected_object={
                    'title':"",
                    'xmin':0,
                    'ymin':0,
                    'xmax':0,
                    'ymax':0,
                    'width':width,
                    'height':height,
                    'image':cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB),
                    'filepath':'',
                    'name':item
                    }
                detected_objects.append(detected_object)
        else:
            annotationTool.createAnnotationFile(
                detected_objects[0]['width'],
                detected_objects[0]['height'],
                detected_objects[0]['xmin'],
                detected_objects[0]['ymin'],
                detected_objects[0]['xmax'],
                detected_objects[0]['ymax'],
                detected_objects[0]['title'],
                item,
                filepath
                )
        return detected_objects
    items=os.listdir(IMAGE_FOLDER_PATH)
    detected_objects_list_f=[]
    for item in items:
        if(item[-4:]=='.jpg'):
            detected_objects_list_f.append(auto_annotate(IMAGE_FOLDER_PATH,item))
    return detected_objects_list_f
    

master = Tk()
master.geometry("700x500")
canvas= Canvas(master)
canvas.place()

frame_top=Frame(master, bg='#add8e6')
frame_top.place(relx=0.01,rely=0.01,relwidth=0.98,relheight=0.28)

frame_left=Frame(master, bg='#add8e6')
frame_left.place(relx=0.01,rely=0.3,relwidth=0.28,relheight=0.69)

frame_right=Frame(master, bg='#add8e6')
frame_right.place(relx=0.30,rely=0.3,relwidth=0.69,relheight=0.69)

detected_objects_list=[]
selected_image=0
imageLabel = Label(frame_right)
def change_image(index):
    img = ImageTk.PhotoImage(Image.fromarray(detected_objects_list[index][0]['image']))
    global selected_image
    selected_image=index
    #imageLabel = Label(frame_right,image=img)
    imageLabel.configure(image=img)
    imageLabel.image = img
    imageLabel.pack(expand=1)

frame_1=Frame(frame_top,bg='white')
frame_1.place(relx=0.01,rely=0.01,relwidth=0.65,relheight=0.2375)
label_ckpt=Label(frame_1, text='Ckpt name:',font='Verdana 8 bold')
label_ckpt.pack(padx=10,pady=10,side=LEFT)

textbox_ckpt=Text(frame_1,height=1.2,width=25)
textbox_ckpt.pack(side=RIGHT)

frame_2=Frame(frame_top,bg='white')
frame_2.place(relx=0.01,rely=0.2575,relwidth=0.65,relheight=0.2375)
label_anno=Label(frame_2, text='Label Map Folder:',font='Verdana 8 bold')
label_anno.pack(padx=10,pady=10,side=LEFT)

textbox_anno=Text(frame_2,height=1.2,width=25)
textbox_anno.pack(side=RIGHT)

frame_3=Frame(frame_top,bg='white')
frame_3.place(relx=0.01,rely=0.5075,relwidth=0.65,relheight=0.2375)
label_model=Label(frame_3, text='Model folder:',font='Verdana 8 bold')
label_model.pack(padx=10,pady=10,side=LEFT)

textbox_model=Text(frame_3,height=1.2,width=25)
textbox_model.pack(side=RIGHT)

frame_4=Frame(frame_top,bg='white')
frame_4.place(relx=0.01,rely=0.7525,relwidth=0.65,relheight=0.2375)
label_image=Label(frame_4, text='Image Folder:',font='Verdana 8 bold')
label_image.pack(padx=10,pady=10,side=LEFT)

textbox_image=Text(frame_4,height=1.2,width=25)
textbox_image.pack(side=RIGHT)

dropbox_option=StringVar(frame_left)
dropbox_option.set("\t")
dropbox_menu=OptionMenu(
    frame_left,
    dropbox_option,
    'deneme'
)

dropbox_menu.pack(padx=10,pady=10,side=TOP)
def start_annotation():
    ckpt=textbox_ckpt.get("1.0",END).split('\n')[0]
    model=textbox_model.get("1.0",END).split('\n')[0]
    image=textbox_image.get("1.0",END).split('\n')[0]
    anno=textbox_anno.get("1.0",END).split('\n')[0]
    
    global detected_objects_list
    #MODEL_PATH,ANNONATION_FOLDER_PATH,IMAGE_FOLDER_PATH,CHECKPOINT_NAME
    detected_objects_list=annotate(model,anno,image,ckpt)
    change_image(0)
    dropbox_option.set("")
    dropbox_menu['menu'].delete(0,'end')
    for i in range(1,len(category_index)+1):
        name=category_index[i]['name']
        dropbox_menu['menu'].add_command(label=name, command=tk._setit(dropbox_option, name))
def change_fn():
    annotationTool.changeAnnotationFile(dropbox_option.get().split('\n')[0] ,detected_objects_list[selected_image][0]['name'], detected_objects_list[selected_image][0]['filepath'])
    return
button_change=Button(frame_left,text="Change label",command=change_fn)
button_change.pack(anchor=S)

frame_left_bottom=Frame(frame_left,bg='white')
frame_left_bottom.place(relx=0.2,rely=0.8,relwidth=0.6,relheight=0.19)
def left_fn():
    global selected_image
    if(selected_image!=0):
        selected_image-=1
        change_image(selected_image)
        
def right_fn():
    global selected_image
    if(selected_image!=len(detected_objects_list)-1):
        selected_image+=1
        change_image(selected_image)
        
button_left=Button(frame_left_bottom,text="<",command=left_fn)
button_left.pack(padx=10,pady=10,side=LEFT)

button_right=Button(frame_left_bottom,text=">",command=right_fn)
button_right.pack(padx=10,pady=10,side=RIGHT)

button_start=Button(frame_top,text="Start Annotation",command=start_annotation)
button_start.pack(padx=10,pady=10,anchor=NE)

master.mainloop()
