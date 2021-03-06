#!/usr/bin/env python
# -*- coding: utf-8 -*-


from keras.models import *
from keras.layers import *
from keras import layers


def u_net(in_left=(64, 64, 1), in_right=(64, 64, 1)):
    """ U-net architecture based on zhixuhao model.

    :param in_left: image corresponding to the left eye.
    :param in_right: image corresponding to the right eye.
    :return: net model.
    """
    left = Input(in_left)
    right = Input(in_right)

    concatenated = layers.concatenate([left, right], axis=-1)

    conv1 = Conv2D(64, 3, padding='same')(concatenated)
    conv1 = Conv2D(64, 3, padding='same')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(128, 3, padding='same')(pool1)
    conv2 = Conv2D(128, 3, padding='same')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(256, 3, padding='same')(pool2)
    conv3 = Conv2D(256, 3, padding='same')(conv3)
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    conv4 = Conv2D(512, 3, padding='same')(pool3)
    conv4 = Conv2D(512, 3, padding='same')(conv4)
    drop4 = Dropout(0.5)(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

    conv5 = Conv2D(1024, 3, padding='same')(pool4)
    conv5 = Conv2D(1024, 3, padding='same')(conv5)
    drop5 = Dropout(0.5)(conv5)

    up6 = Conv2D(512, 2, padding='same')(UpSampling2D(size=(2, 2))(drop5))
    merge6 = concatenate([drop4, up6], axis=3)
    conv6 = Conv2D(512, 3, padding='same')(merge6)
    conv6 = Conv2D(512, 3, padding='same')(conv6)

    up7 = Conv2D(256, 2, padding='same', )(UpSampling2D(size=(2, 2))(conv6))
    merge7 = concatenate([conv3, up7], axis=3)
    conv7 = Conv2D(256, 3, padding='same')(merge7)
    conv7 = Conv2D(256, 3, padding='same')(conv7)

    up8 = Conv2D(128, 2, padding='same', )(UpSampling2D(size=(2, 2))(conv7))
    merge8 = concatenate([conv2, up8], axis=3)
    conv8 = Conv2D(128, 3, padding='same')(merge8)
    conv8 = Conv2D(128, 3, padding='same')(conv8)

    up9 = Conv2D(64, 2, padding='same')(UpSampling2D(size=(2, 2))(conv8))
    merge9 = concatenate([conv1, up9], axis=3)
    conv9 = Conv2D(64, 3, padding='same')(merge9)
    conv9 = Conv2D(64, 3, padding='same')(conv9)
    conv9 = Conv2D(2, 3, padding='same')(conv9)

    conv10 = Conv2D(1, 1, activation='sigmoid', padding='same')(conv9)

    model = Model([left, right], conv10)

    return model
