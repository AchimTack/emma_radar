# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
from subprocess import check_output
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageOps

def frames_to_video(inputpath,outputpath,fps):
    ffmpeg_path = r'E:\Profil\Downloads\ffmpeg\bin\ffmpeg.exe'
    cmd = ffmpeg_path +' -ss 00:00:00 -t 00:00:15 -i "'+ inputpath + '" -vf ' + 'fps='+ str(fps) +' "'+ outputpath +'\out%d.png"'
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
            img = cv2.imread(os.path.join(in_folder, file))
            blur_score = (estimate_blur(img, threshold=100)[1])
            if blur_score < 65:
                print(file)
                os.remove(os.path.join(in_folder, file))
                
def improve_images(in_folder, outpath_processed):
    for file in os.listdir(in_folder):
        if file.endswith(".png"):
            img = Image.open(os.path.join(in_folder, file))

            img = img.crop(
                (
                    170,
                    80,
                    3670,
                    2080
                )
            )

            img1 = img.filter(ImageFilter.EDGE_ENHANCE)
            img2 = img.filter(ImageFilter.DETAIL)
            img = Image.blend(img1, img2, alpha=0.5)

            # create mask: TODO: has to be deeply refactored...
            mask = img.convert("RGBA")
            datas = mask.getdata()
            
            newData = []
            for item in datas:
                if item[0] >= 100 and item[1] >= 100 and item[2] >= 190:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append((0, 0, 0, 255))
            mask.putdata(newData)
            
            draw = ImageDraw.Draw(mask)
            draw.polygon(((0, 1000), (0, 1900), (3400, 1900), (3400, 1000)), fill='white')
            
            blue = Image.new('RGB', (3500,2000), (255, 255, 255))
            img = Image.composite(img, blue, mask)
            
            draw = ImageDraw.Draw(img)
            draw.polygon(((1200, 0), (1700, 800), (1850, 800), (2150, 0)), fill='white')
            
            basewidth = 2000
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize))
            
            img.save(os.path.join(outpath_processed, file))

inputpath = r"Z:\Shared Videos\Structure from Motion\20180509_173633.mp4"
outpath =  r'C:\Users\Achim\Desktop\sfm_test\out'
outpath_processed = r'C:\Users\Achim\Desktop\sfm_test\out_processed'
fps = 20
#frames_to_video(inputpath, outpath, fps)
#del_blurry_img(outpath)
improve_images(outpath, outpath_processed)