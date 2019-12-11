from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import FileSerializer,EmployeeSerializer
from rest_framework.parsers import FileUploadParser
import os
from PIL import Image
import numpy as np
from skimage import transform
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

from tensorflow.keras.preprocessing import image


# from . import millets
# graph = tf.get_default_graph()
# from tensorflow.keras.preprocessing.image import img_to_array
# print("curdir", os.getcwd())
# objmodel = load_model('webapp/RESNET50')
# ALL_PROBABLE_TAGS = {'matchstick', 'hair_slide', 'nematode', 'cleaver', 'ballpoint', 'nail', 'oboe'}
ACCEPTED_TAGS = {'ant', 'seashore', 'hen-of-the-woods','porcupine', 'honeycomb', 'African_chameleon', 'ear', 'corn', 'lakeside', 'sulphur_butterfly', 'ground_beetle', 'stole', 'stinkhorn', 'leaf_beetle', 'bittern'}
# TAGS_COUNTED = {'nematode': 96, 'cleaver': 95, 'matchstick': 6, 'oboe': 77, 'ballpoint': 5, 'hair_slide': 8, 'dishwasher': 1} #out of 96 millet images
# Create your views here.
'''
[('European_gallinule', 1), ('agama', 1), ('balloon', 1), ('beacon', 1), ('bolete', 1), ('bow', 1), ('brain_coral', 1), ('brambling', 1), ('broom', 1), ('cardoon', 1), ('cellular_telephone', 1), ('chime', 1), ('coil', 1), ('coucal', 1), ('cucumber', 1), ('dowitcher', 1), ('flat-coated_retriever', 1), ('fountain', 1), ('frilled_lizard', 1), ('geyser', 1), ('goldfinch', 1), ('green_mamba', 1), ('hair_slide', 1), ('hare', 1), ('harvestman', 1), ('hip', 1), ('hognose_snake', 1), ('honeycomb', 1), ('horned_viper', 1), ('kite', 1), ('leaf_beetle', 1), ('limpkin', 1), ('long-horned_beetle', 1), ('milk_can', 1), ('monarch', 1), 
('mongoose', 1), ('nematode', 1), ('obelisk', 1), ('ostrich', 1), ('picket_fence', 1), ('pineapple', 1), ('sea_anemone', 1), ('snowmobile', 1), ('sundial', 1), ('swing', 1), ('tailed_frog', 1), ('tick', 1), ('weasel', 1), ('whiptail', 1), ('acorn', 2), ('artichoke', 2), ('cabbage_butterfly', 2), ('grasshopper', 2), ('hen-of-the-woods', 2), ('king_crab', 2), ('maze', 2), ('partridge', 2), ('thatch', 2), ('thresher', 2), ('vase', 2), ("yellow_lady's_slipper", 2), ('banana', 3), ('bittern', 3), ('bustard', 3), ('hay', 3), ('worm_fence', 3), ('common_newt', 4), ('knot', 4), ('prairie_chicken', 4), ('sulphur_butterfly', 4), ('earthstar', 5), ('buckeye', 6), ('pot', 7), ('ringlet', 7), ('stinkhorn', 7), ('coral_fungus', 8), ('coral_reef', 8), ('African_chameleon', 12), ('lakeside', 15), ('corn', 45), ('ear', 64)]
'''
class EmployeeList(APIView):
    def get(self, request):
        empList = Employee.objects.all()
        serialized = EmployeeSerializer(empList, many = True)
        return Response(serialized.data)

def load(filename):
   np_image = Image.open(filename)
   np_image = np.array(np_image).astype('float32')/255
   np_image = transform.resize(np_image, (224, 224, 3))
   np_image = np.expand_dims(np_image, axis=0)
   return np_image

def loadForRes(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    actualImage = image.img_to_array(img)
    actualImage = np.expand_dims(actualImage, axis=0)
    actualImage = preprocess_input(actualImage)
    return actualImage

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)


    def post(self, request, *args, **kwargs):   
        print("got request")

        # print("curdir", os.getcwd())
        # model = load_model('/mnt/Data/IIIT/5th sem/mini project/djangorest/djangorest/webapp/googlenet_flower.h5')
        model = load_model('webapp/DiseasesMillets.h5')
        
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            print(file_serializer.data)
            image = load(file_serializer.data["file"][1:])
            # imageForRes = loadForRes(file_serializer.data["file"][1:])
            # objRes = objmodel.predict(imageForRes)
            # tempTags = set(map(lambda x: x[1],decode_predictions(objRes, top=3)[0]))
            # print("tags of image", tempTags)
            # print("valid tags", tempTags & ACCEPTED_TAGS)
            # if len(tempTags & ACCEPTED_TAGS) <= 0:
            #     mainRes = {"isPlant": False, }
            # else:
            res=[]
            # with graph.as_default():
            #  y = model.predict(X)
            res = model.predict(image)
            mainResIndex = np.argmax(res[2])
            # if(mainResIndex==0): #healthy
            #     # mainRes = res[2][0][mainResIndex]
            #     mainRes = {"result": True, "message":"healthy", "prob":res[2][0][mainResIndex]}
            if(mainResIndex==1):
                mainRes = {"isPlant": True, "result": False, "message":"unhealthy", "prob":res[2][0][mainResIndex], "disease":"bacterial"}
            elif(mainResIndex==3):
                mainRes = {"isPlant": True, "result": False, "message":"unhealthy", "prob":res[2][0][mainResIndex], "disease":"ergot"}
            elif(mainResIndex==4):
                mainRes = {"isPlant": True, "result": False, "message":"unhealthy", "prob":res[2][0][mainResIndex], "disease":"rust"}
            elif(mainResIndex==5):
                mainRes = {"isPlant": True, "result": False, "message":"unhealthy", "prob":res[2][0][mainResIndex], "disease":"smut"}
            else:
                mainRes = {"isPlant": True, "result": True, "message":"healthy", "prob":res[2][0][mainResIndex]}

            print("result",  mainRes)
            return Response(mainRes, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
