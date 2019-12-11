from PIL import Image
import numpy as np
from skimage import transform
import numpy as np
import tensorflow as tf
# graph = tf.get_default_graph()
from tensorflow.keras.models import load_model
import os

import tensorflow.keras
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

def load(filename):
   np_image = Image.open(filename)
   np_image = np.array(np_image).astype('float32')/255
   np_image = transform.resize(np_image, (224, 224, 3))
   np_image = np.expand_dims(np_image, axis=0)
   return np_image


# model = ResNet50(weights='webapp/resnet50_weights_tf_dim_ordering_tf_kernels.h5')

# img_path = 'media/bacterial.jpg'
# img = image.load_img(img_path, target_size=(224, 224))
# x = image.img_to_array(img)
# x = np.expand_dims(x, axis=0)
# x = preprocess_input(x)

# model = load_model('/mnt/Data/IIIT/5th sem/mini project/djangorest/djangorest/webapp/googlenet_flower.h5')
objmodel = load_model('webapp/RESNET50')
res=[]
tags = set()
dic ={}
path=os.getcwd() + "/DiseasesMillets/Train/ergot"
images = []
print(os.path.abspath(path))
i=0
for file in os.listdir(path):
    # image = load("DiseasesMillets/Train/Healthy/"+file)
    img_path = "DiseasesMillets/Train/ergot/"+file
    img = image.load_img(img_path, target_size=(224, 224))
    actualImage = image.img_to_array(img)
    actualImage = np.expand_dims(actualImage, axis=0)
    actualImage = preprocess_input(actualImage)
    res = objmodel.predict(actualImage)
    tempTags = list(map(lambda x: x[1],decode_predictions(res, top=3)[0]))
    for item in tempTags:
        if(item in dic):
            dic[item]+=1
        else:
            dic[item] = 1
    i+=1
    # tags = tags | set(tempTags)
    # i+=1
    print(dic)
    # if(i==5):
    #     break
    # images.append(file)
# preds = model.predict(image)
print(sorted(dic.items(), key = lambda kv:(kv[1], kv[0])))   
print("total objects" ,str(i) )
print(dic.keys())
