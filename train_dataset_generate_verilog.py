import numpy as np
import matplotlib.pyplot as plt
import image_dataset_reader
import perceptron
import perceptron_config
import verilog_generator
import sys

train_reader = image_dataset_reader.general_image_reader()
test_set_reader = image_dataset_reader.general_image_reader(dataset_path = "./dataset/")

my_perceptron = perceptron.perceptron()
my_perceptron.train(train_reader)
my_perceptron.quantize()
test_set_accy = my_perceptron.test(test_set_reader)
print("Accuracy on test set:", test_set_accy)

weights_to_save = my_perceptron.weights[:-1]
biased_weight = my_perceptron.weights[-1]
print("Visualizing weights...")
plt.imshow(my_perceptron.weights[:-1].reshape(perceptron_config.weight_mat_height, perceptron_config.weight_mat_width), cmap = "jet")
plt.colorbar()
plt.show()
a = input("Press any key to continue")

save_ = sys.stdout
sys.stdout = open("weight_lut.sv", "w")
verilog_generator.main(weights_to_save)
sys.stdout = save_