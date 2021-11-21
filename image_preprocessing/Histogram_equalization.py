import cv2
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from IPython.display import display
import os
import argparse


my_parser = argparse.ArgumentParser()
my_parser.add_argument('--dir_path', action='store', type=str, required=True)
my_parser.add_argument('--export_path', action='store', type=str, required=True)

args = my_parser.parse_args()

list_class_dir =  os.listdir(args.dir_path)

for l_c_d in list_class_dir:
    if l_c_d == '.DS_Store':
            continue
        
    class_dir_path = os.path.join(args.dir_path, l_c_d)

    if not os.path.exists(os.path.join(args.export_path, l_c_d)):
        os.makedirs(os.path.join(args.export_path, l_c_d))
    
    image_number = 0

    for i_p in os.listdir(class_dir_path):
        if i_p =='.DS_Store':
            continue

        img_path = os.path.join(class_dir_path, i_p)
        print("processing: ", img_path)
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        equ = cv2.equalizeHist(gray)

        equ_dir_path = os.path.join(args.export_path, l_c_d, "equ_{l_c_d}_{image_number}.png".format(l_c_d=l_c_d, image_number=image_number))
        print("export: ", equ_dir_path)
        cv2.imwrite(equ_dir_path, equ)
        image_number += 1
