import shutil, os
import glob
import math
from PIL import Image
from random import shuffle
import tkinter, tkinter.constants, tkinter.filedialog
import yaml


def askDialog():
    return tkinter.filedialog.askdirectory()


def make_yaml(src_path,dest_path):
    with open(src_path + '/data_config.yaml') as file:
        documents = yaml.full_load(file)

    for item, doc in documents.items():
        if (item == "names"):
            item_names = doc
        if (item == "nc"):
            item_nc = doc

    data_file = open(dest_path + "/data.yaml","w")
    lines = ["train: /home/victor/data/" + os.path.basename(dest_path) + "/train/images\n",
    "val: /home/victor/data/" + os.path.basename(dest_path) + "/valid/images\n",
    "test: /home/victor/data/" + os.path.basename(dest_path) + "/test/images\n","\n",
    "nc: {}\n".format(item_nc),
    "names: {}".format(item_names)]
    data_file.writelines(lines)


def split_pictures(coef_train,coef_valid,coef_test):

    print("Please choose an input directory")
    print("You have to select the directory with data_config.yaml, images and labels directories")
    src_path = askDialog()

    print("Please choose the destination directory")
    dest_path = askDialog()

    #shuffle files to get a list
    files_temp = glob.glob(src_path + "/images/train/" + "*.jpg")
    files = []

    #get rid of the extension to shuffle both folders with the same names
    for i in range(len(files_temp)):
        name_temp = files_temp[i]
        name_temp_2 = name_temp[:-4]
        name = name_temp_2[len(src_path + "/images/train/"):]
        files.append(name)

    shuffle(files)

    files_images = []
    files_labels = []
    files_images_path = src_path + "/images/train/"
    files_labels_path = src_path + "/labels/train/"

    for i in range(len(files)):
        name_temp = files[i]
        name_images = files_images_path + name_temp + ".jpg"
        name_labels = files_labels_path + name_temp + ".txt"
        files_images.append(name_images)
        files_labels.append(name_labels)

    #get the number of images for the different directories
    nb_files = len(glob.glob(src_path + "/images/train/" + "*.jpg"))
    nb_train = round(coef_train * nb_files)
    nb_valid = round(coef_valid * nb_files)
    nb_test = round(coef_test * nb_files)

    if ((nb_train + nb_valid + nb_test) > nb_files):
        nb_test -= 1
    elif ((nb_train + nb_valid + nb_test) < nb_files):
        nb_test += 1

    print("Number of files : ",nb_files)
    print("Number of train files : ",nb_train)
    print("Number of valid files : ",nb_valid)
    print("Number of test files : ",nb_test)

    #create directories
    dest_train = dest_path + "/train"
    dest_valid = dest_path + "/valid"
    dest_test = dest_path + "/test"

    try:
        os.mkdir(dest_path)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_path)

    try:
        os.mkdir(dest_train)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_train)

    try:
        os.mkdir(dest_valid)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_valid)

    try:
        os.mkdir(dest_test)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_test)

    #create image and labels directories

    dest_train_images = dest_train + "/images"
    dest_train_labels = dest_train + "/labels"
    dest_valid_images = dest_valid + "/images"
    dest_valid_labels = dest_valid + "/labels"
    dest_test_images = dest_test + "/images"
    dest_test_labels = dest_test + "/labels"

    try:
        os.mkdir(dest_train_images)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_train_images)

    try:
        os.mkdir(dest_train_labels)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_train_labels)

    try:
        os.mkdir(dest_valid_images)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_valid_images)

    try:
        os.mkdir(dest_valid_labels)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_valid_labels)

    try:
        os.mkdir(dest_test_images)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_test_images)

    try:
        os.mkdir(dest_test_labels)
    except OSError:
        print ("Creation of the directory %s failed or it already exists" % dest_test_labels)

    #put the images in the directories
    for i in range(len(files_images)):
        if i < nb_train:
            if not os.path.exists(dest_train_images + '/' + os.path.basename(files_images[i])): #manage file duplicates
                shutil.move(files_images[i], dest_train_images)
        elif i < nb_valid + nb_train:
            if not os.path.exists(dest_valid_images + '/' + os.path.basename(files_images[i])):
                shutil.move(files_images[i], dest_valid_images)
        else:
            if not os.path.exists(dest_test_images + '/' + os.path.basename(files_images[i])):
                shutil.move(files_images[i], dest_test_images)

    #put the labels in the directories
    for i in range(len(files_labels)):
        if i < nb_train:
            if not os.path.exists(dest_train_labels + '/' + os.path.basename(files_labels[i])):
                shutil.move(files_labels[i], dest_train_labels)
        elif i < nb_valid + nb_train:
            if not os.path.exists(dest_valid_labels + '/' + os.path.basename(files_labels[i])):
                shutil.move(files_labels[i], dest_valid_labels)
        else:
            if not os.path.exists(dest_test_labels + '/' + os.path.basename(files_labels[i])):
                shutil.move(files_labels[i], dest_test_labels)

    #make yaml
    make_yaml(src_path,dest_path)


def check_float(potential_float):
    try:
        float(potential_float)
        #print("c'est true")
        return True
    except ValueError:
        #print("c'est false")
        return False


def coeffs():

    coef_train = 0.7
    coef_valid = 0.2
    coef_test = 0.1

    choice = input("Do you want to use custom coefficients for train/valid/test (y/n):")

    if (choice == 'y'):
        print("Please write float number like this : 0.7")
        print("You have to put numbers for the sum of them to be 1")
        coef_train = input("train :")
        coef_valid = input("valid :")
        coef_test = input("test :")

    while not check_float(coef_train) or not check_float(coef_valid) or not check_float(coef_test):
        print("Please use floats for the coefficients :")
        coef_train = input("train :")
        coef_valid = input("valid :")
        coef_test = input("test :")

    coef_train = float(coef_train)
    coef_valid = float(coef_valid)        
    coef_test = float(coef_test)

    lil_sum = round((coef_train + coef_valid + coef_test),12)

    while lil_sum != 1:
        print("Please enter numbers whose sum is equal to one :")
        coef_train = input("train :")
        coef_valid = input("valid :")
        coef_test = input("test :")
        if not check_float(coef_train) or not check_float(coef_valid) or not check_float(coef_test):
            continue

        coef_train = float(coef_train)
        coef_valid = float(coef_valid)        
        coef_test = float(coef_test)
        lil_sum = round((coef_train + coef_valid + coef_test),12)

    return coef_train, coef_valid, coef_test


def labels_to_list(src_path):
    with open(src_path, mode="r") as f:
        data = f.read().split('\n')

    data = [i.split(' ') for i in data]

    #convert to float
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])

    #convert to nice format for bounding boxes in albumentations
    #first we make a new list with only the class ids
    ids = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            ids.append(data[i][0])
        #then we delete the id from the first list
        del data[i][0]
    return ids,data


def main():

    print("Welcome to the split script, you are about to split your dataset from Supervisely to support Yolov5 format")

    coef_train, coef_valid, coef_test = coeffs()
    split_pictures(coef_train, coef_valid, coef_test)
    




main()




