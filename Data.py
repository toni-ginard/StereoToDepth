from keras.preprocessing.image import ImageDataGenerator
from numpy import *
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
import os


def adjust_data():
    """ Adjust data for data segmentation.

    :return: ImageDataGenerator object.
    """
    return ImageDataGenerator(rescale=1./255)


def get_train_generator(l_path, r_path, d_path, in_size, batch_size):
    l_datagen = adjust_data()
    r_datagen = adjust_data()
    d_datagen = adjust_data()
    l_generator = l_datagen.flow_from_directory(l_path,
                                                class_mode=None,
                                                color_mode='grayscale',
                                                target_size=(in_size, in_size),
                                                batch_size=batch_size,
                                                shuffle=False)

    r_generator = r_datagen.flow_from_directory(r_path,
                                                class_mode=None,
                                                color_mode='grayscale',
                                                target_size=(in_size, in_size),
                                                batch_size=batch_size,
                                                shuffle=False)

    d_generator = d_datagen.flow_from_directory(d_path,
                                                class_mode=None,
                                                color_mode='grayscale',
                                                target_size=(in_size, in_size),
                                                batch_size=batch_size,
                                                shuffle=False)

    in_generator = zip(l_generator, r_generator)
    train_generator = zip(in_generator, d_generator)
    for (in_img, d_img) in train_generator:
        yield([in_img[0], in_img[1]], d_img)


def get_test_generator(l_path, r_path, in_size, batch_size):
    l_datagen = adjust_data()
    r_datagen = adjust_data()

    l_generator = l_datagen.flow_from_directory(l_path,
                                                class_mode=None,
                                                color_mode='grayscale',
                                                target_size=(in_size, in_size),
                                                batch_size=batch_size,
                                                shuffle=False)

    r_generator = r_datagen.flow_from_directory(r_path,
                                                class_mode=None,
                                                color_mode='grayscale',
                                                target_size=(in_size, in_size),
                                                batch_size=batch_size,
                                                shuffle=False)
    test_generator = zip(l_generator, r_generator)
    for (l_img, r_img) in test_generator:
        yield[l_img, r_img]


def save_validation(history, path):
    """ Save a graphic for our training's loss and validation loss. Y axis is in logarithmic scale.

    :param history: History object. Its `History.history` attribute is a record of training loss
        and validation loss values at successive epochs.
    :param path: directory where to store the graphic.
    """
    loss = []
    val_loss = []

    for i in history:
        loss += i.history['loss']
        val_loss += i.history['val_loss']

    epochs = range(1, len(loss) + 1)
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')

    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.yscale('log')
    plt.legend()
    plt.savefig(path)


def save_summary(model, path):
    """ Save summary of a model in the specified path.

    :param model: net model.
    :param path: directory where to store the summary.
    """
    open(os.path.join(path, 'summary.txt'), 'w')
    with open(path + '/' + 'summary.txt', 'w') as f:
        with redirect_stdout(f):
            model.summary()


def save_predictions(path, num_images, predictions):
    """ Save predictions made from a model.

    :param path: directory where to store the predictions.
    :param int num_images: number of predictions made.
    :param predictions: numpy.array
    """
    if num_images > 0:
        for i in range(num_images):
            name = path + "/pred" + str(i) + ".png"
            plt.imsave(name, predictions[i], cmap='gray')
