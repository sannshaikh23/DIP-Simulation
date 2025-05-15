from flask import Flask, request, send_from_directory
import cv2
import os
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static'

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file1 = request.files['img1']
    file2 = request.files['img2']
    file_rotate=request.files['img_rotate']
    file_translate=request.files['img_translate']

    path1 = os.path.join(UPLOAD_FOLDER, 'img1.png')
    path2 = os.path.join(UPLOAD_FOLDER, 'img2.png')
    path3 = os.path.join(UPLOAD_FOLDER, 'img_rotate')
    path4 = os.path.join(UPLOAD_FOLDER, 'img_translate')
    file1.save(path1)
    file2.save(path2)
    file_rotate.save(path3)
    file_translate.save(path4)

    i1 = cv2.imread(path1)
    i2 = cv2.imread(path2)
    i1 = cv2.resize(i1, (300, 168))
    i2 = cv2.resize(i2, (300, 168))
    
    img_rotate=cv2.imread(path3)
    img_translate=cv2.imread(path4)
    # img_rotate= cv2.resize(img_rotate, (300, 168))
    img_translate= cv2.resize(img_translate, (900, 1000))

    # Delete previous output images (if any)
    for fname in ['i1.png', 'i2.png', 'add.png', 'sub.png','rotated_image.png','translated_image.png']:
        fpath = os.path.join(OUTPUT_FOLDER, fname)
        if os.path.exists(fpath):
            os.remove(fpath)

    add = cv2.add(i1, i2)
    sub = cv2.subtract(i1, i2)
    # rotation
    height,width=img_rotate.shape[:2]
    center=(width/2,height/2)
    rotate_matrix=cv2.getRotationMatrix2D(center=center,angle=45,scale=1)
    rotated_image=cv2.warpAffine(src=img_rotate,M=rotate_matrix,dsize=(width,height))
    # translation
    translation_matrix=np.float32([[1,0,30],[0,1,30]])
    translated_image=cv2.warpAffine(img_translate,translation_matrix,(width,height))

    cv2.imwrite(os.path.join(OUTPUT_FOLDER, 'i1.png'), i1)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, 'i2.png'), i2)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, 'add.png'), add)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, 'sub.png'), sub)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, 'rotated_image.png'), rotated_image)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, 'translated_image.png'),  translated_image)

    return send_from_directory('.', 'index.html')



@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)
