import numpy as np
import os
import random
import cv2
import perceptron_config

normalize_gray_avg = 100

#virtual image reader
class general_image_reader:
    def __init__(self, dataset_path = "./dataset/"):
        self.img_array = []
        self.label_array = []
        temp_name_label_holder = []
        negative_sample_path = dataset_path + "0/"
        negative_samples = [os.path.join(dp, f) for dp, dn, filenames in os.walk(negative_sample_path) for f in filenames if f.endswith(".jpg")]
        for i in negative_samples:
            print("Processing file:", i)
            temp_name_label_holder.append((i, -1))
        positive_sample_path = dataset_path + "1/"
        positive_samples = [os.path.join(dp, f) for dp, dn, filenames in os.walk(positive_sample_path) for f in filenames if f.endswith(".jpg")]
        for i in positive_samples:
            print("Processing file:", i)
            temp_name_label_holder.append((i, 1))
        random.shuffle(temp_name_label_holder)
        random.shuffle(temp_name_label_holder)
        for path, label in temp_name_label_holder:
            image = cv2.imread(path, 0)
            self.img_array.append(self.preprocess(image))
            self.label_array.append(label)
        self.data_set_length = len(self.img_array)
        print("Reader data length:", self.data_set_length)
        assert(len(self.img_array) == len(self.label_array))
        self.reset()
    
    def preprocess(self, img_array):
        #img array is 2-D uint8 array (grayscale)
        img_array = cv2.resize(img_array, (perceptron_config.weight_mat_height, perceptron_config.weight_mat_width))
        return np.array(img_array >= normalize_gray_avg, dtype = "uint8") # * 255
    
    def reset(self):
        self.read_ptr = -1

    #return np.array(img), label
    def get_one(self):
        self.read_ptr += 1
        return [self.img_array[self.read_ptr], self.label_array[self.read_ptr]]

    def get_length(self):
        return self.data_set_length

    def get_all(self):
        ret = []
        for i in range(self.get_length()):
            ret.append(self.get_one())
        return ret