# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
from subprocess import check_output
from PIL import Image, ImageFilter

def frames_to_video(inputpath,outputpath,fps):
    ffmpeg_path = r'E:\Profil\Downloads\ffmpeg\bin\ffmpeg.exe'
    cmd = ffmpeg_path +' -ss 00:00:01 -t 00:00:5 -i "'+ inputpath + '" -vf ' + 'fps='+ str(fps) +' "'+ outputpath +'\out%d.png"'
    print(cmd)
    check_output(cmd , shell=True).decode()

#Source: https://gist.github.com/murarikrishna/f676bfdad9e2eabaef84b0e18873f596
def estimate_blur(image, threshold=100):
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_map = cv2.Laplacian(image, cv2.CV_64F)
    score = np.var(blur_map)
    return blur_map, score, bool(score < threshold)

def del_blurry_img(in_folder):
    for file in os.listdir(in_folder):
        if file.endswith(".png"):
            print(file)
            img = cv2.imread(os.path.join(in_folder, file))
            blur_score = (estimate_blur(img, threshold=100)[1])
            if blur_score < 65:
                os.remove(os.path.join(in_folder, file))
                
def improve_images(in_folder):
    for file in os.listdir(in_folder):
        if file.endswith(".png"):
            image = Image.open(os.path.join(in_folder, file))
            image = image.filter(ImageFilter.FIND_EDGES)
            image.save(os.path.join(outpath_processed, file))

inputpath = r'"C:\Users\Achim\Desktop\sfm_test\in\20180509_071426.mp4"'
outpath =  r'C:\Users\Achim\Desktop\sfm_test\out'
outpath_processed = r'C:\Users\Achim\Desktop\sfm_test\out_processed'
fps = 5
frames_to_video(inputpath,outpath,fps)
del_blurry_img(outpath)