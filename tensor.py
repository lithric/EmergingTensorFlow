from pickletools import optimize
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from PyDictionary import PyDictionary

dictionary = PyDictionary()
"""
AI Questions:
1. is the input a real sentence with understandable words?
    ex(yes): me how, not, before gone fiewojios.
    ex(yes): iewojf, ni, siofr bad goof.
    ex(yes): ewweofk@ji iab!@ efo nice
    ex(no): iojfre efiwojfi, ireofj weow.
2. does the sentence have a flow to it?
    ex(yes): @{I have never been} over to real good things without purpose.
    ex(yes): begin! @{has just now} be before no.
    ex(no): eopkeowp nice is opewkop don't.
    ex(no): me how, not, before gone fiewojios.
"""

print("TensorFlow version:", tf.__version__)

# gets a dataset that contains 70,000 28x28 greyscale images of clothing
fashion_mnist = tf.keras.datasets.fashion_mnist


#region#*seperate the data into parts
(train_images, #array of training images: 60,000u^2: 784u
train_labels #array of training labels: 60,000u
),(
test_images, #array of images used for the testing phase: 10,000u^2: 784u
test_labels #array of labels used for the testing phase: 10,000u
) = fashion_mnist.load_data() # loads the data
#endregion

#prepare data
train_images = train_images / 255.0
test_images = test_images / 255.0

class_names = ['T-shirt/top', 'Trouser','Pullover','Dress','Coat','Sandal',
'Shirt','Sneaker','Bag','Ankle boot']

model = tf.keras.Sequential([
    layers.Flatten(input_shape=(28,28)), # first layer: contains inputs
    layers.Dense(60, activation='relu'), # second layer: evaluates inputs
    layers.Dense(300, activation='relu'), # second layer: evaluates inputs
    layers.Dense(60, activation='relu'), # second layer: evaluates inputs
    layers.Dense(10) # final layer: contains outputs
])

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

model.fit(train_images, train_labels, epochs=10)

test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)

print('\nTest accuracy:', test_acc)

#model is now trained

probability_model = tf.keras.Sequential([
    model,
    layers.Softmax()
])

predictions = probability_model.predict(test_images)

def plot_image(i, predictions_array, true_label, img):
    true_label, img = true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
    100*np.max(predictions_array),
    class_names[true_label]),
    color=color)

def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10))
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color="#777777")
    plt.ylim([0,1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2*num_cols, 2*i+1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(num_rows, 2*num_cols, 2*i+2)
    plot_value_array(i, predictions[i],test_labels)
plt.tight_layout()
plt.show()