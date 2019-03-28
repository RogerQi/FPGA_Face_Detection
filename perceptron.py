import numpy as np
import os
import sys
import perceptron_config
import time
import matplotlib.pyplot as plt
from IPython import embed

#virtual image reader
class digit_image_reader:
    def __init__(self, file_path, single_digit = -1):
        self.img_array = []
        self.label_array = []
        row_ptr = 0
        cur_img = []
        with open(file_path) as f:
            while True:
                row_ptr += 1
                line = f.readline()
                if not line: break
                if row_ptr % 33 == 0: #label line!
                    label = int(line.strip("\n "))
                    if single_digit != -1 and label != single_digit:
                        cur_img = []
                        continue
                    self.img_array.append(np.array(cur_img))
                    self.label_array.append(label)
                    cur_img = []
                else:
                    cur_img.append([int(i) for i in line.strip("\n ")])
        self.data_set_length = len(self.img_array)
        print("Reader data length:", self.data_set_length)
        assert(len(self.img_array) == len(self.label_array))
        self.reset()
    
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

#with biased variable
total_weight_num = perceptron_config.weight_mat_width * perceptron_config.weight_mat_height + 1

def sign(num):
    if num > 0:
        return 1
    return -1

#single class perceptron
class perceptron:
    def __init__(self, learning_rate_constant = 0.1, epoch_limit = 30):
        self.c = learning_rate_constant
        self.epoch = 0
        self.weights = np.random.normal(0, 1, size = total_weight_num)
        self.epoch_limit = epoch_limit

    def single_predict(self, feature):
        return sign(np.dot(self.weights, feature))
    
    def train(self, reader_obj_ptr):
        for i in range(self.epoch_limit):
            correct_prediction = 0
            for j in range(reader_obj_ptr.get_length()):
                img, label = reader_obj_ptr.get_one()
                #print(img.shape)
                # if label == 0: #set to tag of desired number
                #     label = 1
                # else:
                #     label = -1
                correct_prediction += self.train_one_img(img, label)
            print("Epoch: {0} Accuracy on training set: {1}".format(i + 1, correct_prediction * 1.0 / reader_obj_ptr.get_length()))
            reader_obj_ptr.reset()
        print("Training complete. Biased weight:", self.weights[-1])
    
    #true label: 1 or -1
    def train_one_img(self, img_array, true_label):
        feature = img_array.flatten()
        feature = np.append(feature, 1)
        predicted_label = self.single_predict(feature)
        if predicted_label != true_label:
            #wrong prediction
            offset_vec = np.dot(self.get_current_learning_rate(), feature)
            if true_label == -1: offset_vec = -offset_vec
            self.weights += offset_vec
            return 0
        return 1
    
    def test(self, reader_obj_ptr):
        total_data_size = reader_obj_ptr.get_length()
        correct_predict_cnt = 0
        for i in range(total_data_size):
            img, label = reader_obj_ptr.get_one()
            #print(img.shape)
            # if label == 0:
            #     label = 1
            # else:
            #     label = -1
            feature = img.flatten()
            feature = np.append(feature, 1)
            predict_label = self.single_predict(feature)
            if predict_label == label: correct_predict_cnt += 1
        return correct_predict_cnt * 1. / total_data_size

    def get_current_learning_rate(self):
        return np.exp(-self.c * self.epoch)
    
    def quantize(self):
        new_weight = [int(i * 1000) for i in self.weights]
        self.weights = np.array(new_weight, dtype = "int16")

class multi_class_perceptron:
    def __init__(self, class_num = 1):
        pass

def main():
    reader = digit_image_reader(file_path = "optdigits-orig_train.txt")
    my_perceptron = perceptron()
    my_perceptron.train(reader)
    print("Min", min(my_perceptron.weights))
    test_reader = digit_image_reader(file_path = "optdigits-orig_test.txt")
    accy = my_perceptron.test(test_reader)
    print("Overall accuracy on test set:", accy)
    test_reader.reset()
    print("First five weights and last five weights")
    print(my_perceptron.weights[:5])
    print(my_perceptron.weights[-5:])
    # embed()
    my_perceptron.quantize()
    print("[Quantized] First five weights and last five weights")
    print(my_perceptron.weights[:5])
    print(my_perceptron.weights[-5:])
    accy = my_perceptron.test(test_reader)
    print("Quantized accuracy:", accy)
    plt.imshow(my_perceptron.weights[:-1].reshape(32, 32), cmap = "jet")
    plt.show()
    a = input()

if __name__ == '__main__':
    main()