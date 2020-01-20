from __future__ import absolute_import, division, print_function, unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import pandas as pd
import os
try:
    print('2x')
except Exception:
  pass
import tensorflow as tf
import seaborn as sns
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from collections import Counter
from imblearn.under_sampling import RandomUnderSampler
from tensorflow.keras import regularizers
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
from django.template import Context, Template




def home(request):
    return render(request,'home1.html')

def predict(request):


    file1=request.POST.get('myfile')

    model = tf.keras.models.load_model('sepsis_improved.h5')
    model.summary()

    # pre = pd.read_csv('Final_Model/p000053.psv',delimiter='|')
    pre = pd.read_csv(file1,delimiter='|')#no sepesis
    length = pre.shape[0]
    print(length)

    pre = pre.interpolate()
    pre = pre.fillna(method='bfill')
    pre = pre.fillna(method='ffill')
    pre = pre.fillna(pre.mean())
    # df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    train = pre
    X_HR = np.array(pre['HR'])#(no_sampels,60,no_features)
    X_Temp = np.array(pre['Temp'])#(no_sampels,60,no_features)
    X_Resp = np.array(pre['Resp'])
    X_WBC = np.array(pre['WBC'])
    X_MAP = np.array(pre['MAP'])
    X_Gender = np.array(pre['Gender'])
    X_Age = np.array(pre['Age'])

    HR=X_HR.tolist()
    TEMP=X_Temp.tolist()
    RESP=X_Resp.tolist()
    WBC=X_WBC.tolist()
    MAP=X_MAP.tolist()
    GENDER=X_Gender.tolist()
    AGE=X_Age.tolist()

    y_original = pre['SepsisLabel']

    temp = np.column_stack((X_HR,X_Temp,X_Resp,X_WBC,X_MAP,X_Gender,X_Age))
    l = len(temp)

    f = ['X_HR','X_Temp','X_Resp','X_WBC','X_MAP','X_Gender','X_Age']

    padded_ip = tf.keras.preprocessing.sequence.pad_sequences([temp],maxlen = 60,padding='post',value=-1)
    y_pad = tf.keras.preprocessing.sequence.pad_sequences([y_original],maxlen = 60,padding='post',value=-1)

    ip = padded_ip.reshape(-1, 60, len(f))

    ip.shape

    y1 = model.predict(padded_ip)

    for i,j in y1[0]:
        first_value=i.tolist()
        second_value=j.tolist()
    # print(y1.shape())

        # first_value=i.tolist()
        # second_value=j.tolist()

        # print(first_value)
        # print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    # y1 = model.predict(padded_ip)
    # for i,j in zip(y1[0],y_original):
    #   print(i,j)



    context={
    'HR':HR,
    'TEMP':TEMP,
    'RESP':RESP,
    'WBC':WBC,
    'MAP':MAP,
    'GENDER':GENDER,
    'AGE':AGE,
    'first_value':first_value,
    # 'second_value':second_value,
    }
    request.session["data_set1_HR"]=HR
    request.session["data_set2_TEMP"]=TEMP
    request.session["data_set3_RESP"]=RESP
    request.session["data_set4_WBC"]=WBC
    request.session["data_set5_MAP"]=MAP
    request.session["data_set6_GENDER"]=GENDER
    request.session["data_set7_AGE"]=AGE
    request.session["data_set8_first_value"]=first_value
    # request.session["data_set9_second_value"]=second_value



    return render(request,'home.html',{"context": context})


# def get_data(request):
#     print("--------------------------")
#     print(request.session['data_chart1'])
#     print(request.session['data_chart2'])
#
#     labels = ["Users", "Blue", "Yellow", "Green", "Purple", "Orange","Users", "Blue", "Yellow", "Green", "Purple", "Orange","Users", "Blue", "Yellow", "Green", "Purple", "Orange"]
#     default_items = request.session['data_chart1']
#     data = {
#             "labels": labels,
#             "default": default_items,
#     }
#     return Response(data)


# def charts_show(request):
#     data=predict(request)
#     print(data)
#
#
#
#



User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts.html')



class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None,allow_nan=False):
        labels = [0, 5, 10, 15, 20, 25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125]
        default_items1 = request.session['data_set1_HR']
        default_items2 = request.session['data_set2_TEMP']
        default_items3 = request.session['data_set3_RESP']
        default_items4 = request.session['data_set4_WBC']
        default_items5 = request.session['data_set5_MAP']
        default_items6 = request.session['data_set6_GENDER']
        default_items7 = request.session['data_set7_AGE']
        # default_items8 = [0, 5, 10, 15, 20, 25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
        # default_items9 = [25,63,56,25,36,22,45,96,12,26,69,85,26,85,69,86,57,69,66,85,45,96]
        data = {
                "labels": labels,
                "default1": default_items1,
                "default2": default_items2,
                "default3": default_items3,
                "default4": default_items4,
                "default5": default_items5,
                "default6": default_items6,
                "default7": default_items7,
                # "default8": default_items8,
                # "default9": default_items9,
        }
        return Response(data)




#
#
#
# class ChartData(APIView):
#     authentication_classes = []
#     permission_classes = []
