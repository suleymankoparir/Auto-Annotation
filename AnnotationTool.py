import xml.etree.ElementTree as ET
import os

    
class AnnotationTool:
    def changeAnnotationFile(self,label,filename,path):
        mytree = ET.parse(path+filename.split('.')[0]+'.xml')
        myroot = mytree.getroot()
        for lbl in myroot.iter('name'):
            lbl.text=label
            break;#multiple name space
        mytree.write(path+filename.split('.')[0]+'.xml')
    def createAnnotationFile(self,annW,annH,annXmin,annYmin,annXmax,annYmax,label,filename,path):
        mytree = ET.parse('template.xml')
        myroot = mytree.getroot()
        
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

