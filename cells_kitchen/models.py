from keras.models import Model
from keras.layers import Input, Conv2D, Conv2DTranspose, MaxPooling2D, Add, UpSampling2D, SpatialDropout2D,\
    concatenate, BatchNormalization
from keras.optimizers import Adam
import keras.backend as K


def unet(input_size, output_channels, filters=32, lr_init=.001, kernel_initializer='glorot_normal', bn=False):
    # unet modified from: https://github.com/zhixuhao/unet/blob/master/model.py

    inputs = Input(input_size)

    conv1 = Conv2D(filters, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(inputs)
    conv1 = Conv2D(filters, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv1)
    conv1 = BatchNormalization()(conv1) if bn else conv1
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(filters*2, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(pool1)
    conv2 = Conv2D(filters*2, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv2)
    conv2 = BatchNormalization()(conv2) if bn else conv2
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(filters*4, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(pool2)
    conv3 = Conv2D(filters*4, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv3)
    conv3 = BatchNormalization()(conv3) if bn else conv3
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

    conv4 = Conv2D(filters*8, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(pool3)
    conv4 = Conv2D(filters*8, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv4)
    conv4 = BatchNormalization()(conv4) if bn else conv4
    drop4 = SpatialDropout2D(0.5)(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

    conv5 = Conv2D(filters*16, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(pool4)
    conv5 = Conv2D(filters*16, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv5)
    conv5 = BatchNormalization()(conv5) if bn else conv5
    drop5 = SpatialDropout2D(0.5)(conv5)

    up6 = Conv2D(filters*8, 2, activation='relu', padding='same', kernel_initializer=kernel_initializer)(
        UpSampling2D(size=(2, 2))(drop5))
    merge6 = concatenate([drop4, up6], axis=3)
    conv6 = Conv2D(filters*8, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(merge6)
    conv6 = Conv2D(filters*8, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv6)
    conv6 = BatchNormalization()(conv6) if bn else conv6

    up7 = Conv2D(filters*4, 2, activation='relu', padding='same', kernel_initializer=kernel_initializer)(
        UpSampling2D(size=(2, 2))(conv6))
    merge7 = concatenate([conv3, up7], axis=3)
    conv7 = Conv2D(filters*4, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(merge7)
    conv7 = Conv2D(filters*4, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv7)
    conv7 = BatchNormalization()(conv7) if bn else conv7

    up8 = Conv2D(filters*2, 2, activation='relu', padding='same', kernel_initializer=kernel_initializer)(
        UpSampling2D(size=(2, 2))(conv7))
    merge8 = concatenate([conv2, up8], axis=3)
    conv8 = Conv2D(filters*2, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(merge8)
    conv8 = Conv2D(filters*2, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv8)
    conv8 = BatchNormalization()(conv8) if bn else conv8

    up9 = Conv2D(filters, 2, activation='relu', padding='same', kernel_initializer=kernel_initializer)(
        UpSampling2D(size=(2, 2))(conv8))
    merge9 = concatenate([conv1, up9], axis=3)
    conv9 = Conv2D(filters, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(merge9)
    conv9 = Conv2D(filters, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv9)
    conv9 = Conv2D(2, 3, activation='relu', padding='same', kernel_initializer=kernel_initializer)(conv9)
    conv9 = BatchNormalization()(conv9) if bn else conv9

    conv10 = Conv2D(output_channels, 1, activation='sigmoid')(conv9)

    # compile
    model = Model(input=inputs, output=conv10, name="unet")
    model.compile(optimizer=Adam(lr=lr_init), loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()

    return model
