import os
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2
import numpy as np
from AnnotationTool import AnnotationTool
class Detect():
    category_index=[]
    def category_index_return(self):
        return category_index
    def annotate(self,MODEL_PATH,ANNONATION_FOLDER_PATH,IMAGE_FOLDER_PATH,CHECKPOINT_NAME):
        annotationTool=AnnotationTool()
        global category_index
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
        category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])
        def auto_annotate(filepath,item):
            img = cv2.imread(filepath+item)
            height=img.shape[0]
            width=img.shape[1]
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
                        max_boxes_to_draw=5,
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
                if len(detected_objects)>1:
                    for i in range(1,len(detected_objects)):
                        annotationTool.addObject(
                            detected_objects[i]['xmin'], 
                            detected_objects[i]['ymin'],
                            detected_objects[i]['xmax'], 
                            detected_objects[i]['ymax'], 
                            detected_objects[i]['title'], 
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