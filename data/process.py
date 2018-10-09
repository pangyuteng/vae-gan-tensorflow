import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk
import os
import hashlib
from PIL import Image

def read(fpath):
    reader= sitk.ImageFileReader()
    reader.SetFileName(fpath)
    img = reader.Execute()
    arr = sitk.GetArrayFromImage(img)    
    spacing = img.GetSpacing()
    origin = img.GetOrigin()
    direction = img.GetDirection()    
    return arr,spacing,origin,direction

def write(fpath,arr,spacing,origin,direction,use_compression=True):
    img = sitk.GetImageFromArray(arr)
    img.SetSpacing(spacing)
    img.SetOrigin(origin)
    img.SetDirection(direction)
    writer = sitk.ImageFileWriter()    
    writer.SetFileName(fpath)
    writer.SetUseCompression(use_compression)
    writer.Execute(img)

fpath_list = [os.path.join('luna16',x) for x in os.listdir('luna16') if x.endswith('.nii.gz')]
for row in fpath_list:
    print(row)

 data = {
    'train_data_list':[],
    'train_lab_list':[],
}

c=0

for n,fpath in enumerate(fpath_list):
    arr,spacing,origin,direction = read(fpath)
    #arr = -1*arr #????
    print(arr.shape,np.max(arr),np.min(arr))
    arr = arr.clip(-1000,1000).astype(float)
    arr = (255*(arr+1000)/2500).astype('uint8')
    for m in range(arr.shape[0]):
        img = arr[m,:].squeeze()
        slicepath = os.path.join(os.path.dirname(fpath),hashlib.sha224(img.tostring()).hexdigest()+'.png')
        img = Image.fromarray(img)
        img.thumbnail((64,64), Image.ANTIALIAS)
        loc = float(m)/arr.shape[0]
        img.save(slicepath)
        data['train_data_list'].append(slicepath)
        data['train_lab_list'].append(loc>0.5)
    c+=1
    #if c > 2:
    #    break
    
import yaml 
with open('data.yml','w') as f:
    f.write(yaml.dump(data))

    
