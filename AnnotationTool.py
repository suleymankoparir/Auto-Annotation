import xml.etree.ElementTree as ET
import os
import copy
    
class AnnotationTool:  
    def changeAnnotationTitle(self,label,filename,path,index):
        mytree = ET.parse(path+filename.split('.')[0]+'.xml')
        myroot = mytree.getroot()
        object_count=0
        for lbl in myroot.iter('name'):
            if lbl.text!='' and lbl.text!=None and lbl.text!='rotation':
                object_count+=1
        
        index=object_count-index-1
        object_count=0
        for lbl in myroot.iter('name'):
            if lbl.text!='' and lbl.text!=None and lbl.text!='rotation':
                if object_count==index:
                    lbl.text=label
                    break
                else:
                    object_count+=1
            #break;#multiple name space
        mytree.write(path+filename.split('.')[0]+'.xml')
    def addObject(self,annXmin,annYmin,annXmax,annYmax,label,filename,path):
        mytree = ET.parse(path+filename.split('.')[0]+'.xml')
        myroot = mytree.getroot()
        
        for c in myroot.findall(".//object"):
            dupe = copy.deepcopy(c)
            myroot.append(dupe)
            break;
        for lbl in myroot.iter('name'):
            lbl.text=label
            break;#multiple name space
        for xmin in myroot.iter('xmin'):
            xmin.text=str(float(annXmin))
            break;
        for ymin in myroot.iter('ymin'):
            ymin.text=str(float(annYmin))
            break;
        for xmax in myroot.iter('xmax'):
            xmax.text=str(float(annXmax))
            break;
        for ymax in myroot.iter('ymax'):
            ymax.text=str(float(annYmax))
            break;
        mytree.write(path+filename.split('.')[0]+'.xml')
        
    def createAnnotationFile(self,annW,annH,annXmin,annYmin,annXmax,annYmax,label,filename,path):
        mytree = ET.parse('template.xml')
        myroot = mytree.getroot()
        #print(annW,annH)
        for lbl in myroot.iter('name'):
            lbl.text=label
            break;#multiple name space
        for fname in myroot.iter('filename'):
            fname.text=filename
        for sizeW in myroot.iter('width'):
            sizeW.text=str(int(annW))
        for sizeH in myroot.iter('height'):
            sizeH.text=str(int(annH))
        for xmin in myroot.iter('xmin'):
            xmin.text=str(float(annXmin))
        for ymin in myroot.iter('ymin'):
            ymin.text=str(float(annYmin))
        for xmax in myroot.iter('xmax'):
            xmax.text=str(float(annXmax))
        for ymax in myroot.iter('ymax'):
            ymax.text=str(float(annYmax)) 
        mytree.write(path+filename.split('.')[0]+'.xml')
######################################################################################