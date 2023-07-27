from django.shortcuts import render
# from .forms import UploadImageForm
# import base64
# # 객체 감지 로직을 import
# # 예: from detection_module import detect_objects
# import cv2
# import matlab.engine
# import numpy as np
# eng = matlab.engine.start_matlab()
# def detect_objects(request):
#     if request.method == 'POST':
#         form = UploadImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#
#             # 이미지 파일 경로
#             image_path = form.instance.image.path
#             print(image_path)
#
#             img = cv2.imread(image_path)
#             img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#             img = cv2.resize(img,(416,416))
#
#             result = eng.detector(img)
#             print(result)
#             for i in list(result):
#                 print(i)
#                 X,Y,W,H = int(i[0]), int(i[1]), int(i[2]), int(i[3])
#                 cv2.rectangle(img,(X,Y),(X+W,Y+H),(0,255,0),2)
#                 print("done")
#             cv2.imwrite("test.png",img)
#             _, buffer = cv2.imencode('.png', img)
#             img_base64 = base64.b64encode(buffer).decode('utf-8')
#
#
#             # 딥러닝 모델을 사용하여 객체 감지 수행
#             # 결과를 얻고 처리하는 로직
#             # 예: results = detect_objects(image_path)
#
#             # 결과를 템플릿에 전달
#             context = {
#                 'results': list(result),
#                 'img_base64': img_base64,
#
#             }
#             return render(request, 'detection_app/detection_results.html', context)
#     else:
#         form = UploadImageForm()
#     return render(request, 'detection_app/upload_image.html', {'form': form})

# detection_app/views.py

from django.http import JsonResponse
from .forms import UploadImageForm
import base64
# 객체 감지 로직을 import
# 예: from detection_module import detect_objects

from rest_framework.decorators import api_view

import cv2
import matlab.engine
import numpy as np
eng = matlab.engine.start_matlab()

def encode_image_to_base64(image):
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')

def detect_objects(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            # 이미지 파일 경로
            image_path = form.instance.image.path
            print(image_path)

            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = cv2.resize(img, (416, 416))

            result = eng.detector(img)
            print(result)
            for i in list(result):
                print(i)
                X, Y, W, H = int(i[0]), int(i[1]), int(i[2]), int(i[3])
                cv2.rectangle(img, (X, Y), (X + W, Y + H), (0, 255, 0), 2)
                print("done")
            cv2.imwrite("test.png", img)

            # 처리된 결과 이미지를 Base64로 인코딩
            img_base64 = encode_image_to_base64(img)

            # 딥러닝 모델을 사용하여 객체 감지 수행
            # 결과를 얻고 처리하는 로직
            # 예: results = detect_objects(image_path)

            # 결과를 템플릿에 전달
            context = {
                'results': list(result),
                'img_base64': img_base64,
            }
            return render(request, 'detection_app/detection_results.html', context)
    else:
        form = UploadImageForm()
    return render(request, 'detection_app/upload_image.html', {'form': form})
