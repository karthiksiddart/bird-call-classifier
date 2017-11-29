#!/usr/bin/env python

from __future__ import print_function

import keras
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Input, concatenate
from keras.layers import Dense, Dropout, Embedding, Flatten, Activation
from keras.layers.normalization import BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard
from keras.layers import PReLU
from keras import regularizers

"""
The model class for a convelutional neural network using keras
"""

xpixels = 138
ypixels = 138

def bird_model(num_classes):


        model = Sequential()
        #input layer
        model.add(Conv2D(32, kernel_size=(3, 3), input_shape=(xpixels, ypixels, 1)))
        model.add(PReLU(alpha_regularizer=regularizers.l2(0.01)))

        #hidden layers
        model.add(Conv2D(64, kernel_size=(3, 3)))
        model.add(PReLU(alpha_regularizer=regularizers.l2(0.01)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(128, kernel_size=(3, 3)))
        model.add(PReLU(alpha_regularizer=regularizers.l2(0.01)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(128, kernel_size=(3, 3)))
        model.add(PReLU(alpha_regularizer=regularizers.l2(0.01)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(BatchNormalization())
        model.add(Dropout(0.25))

        model.add(Conv2D(128, kernel_size=(3, 3)))
        model.add(PReLU(alpha_regularizer=regularizers.l2(0.01)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(BatchNormalization())
        model.add(Dropout(0.25))

        model.add(Conv2D(128, kernel_size=(3, 3)))
        model.add(PReLU(alpha_regularizer=regularizers.l2(0.01)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(BatchNormalization())
        model.add(Dropout(0.25))

        #MLP
        model.add(Flatten())
        model.add(Dense(128))
        model.add(PReLU(alpha_regularizer=regularizers.l2(0.01)))
        model.add(Dropout(0.5))

        #output layer
        model.add(Dense(num_classes))
        model.add(Activation('softmax'))


        return model

def get_time_str():
    """
    Utility function to return timestamp string to append to log and
    weight output files
    """
    from datetime import datetime
    t_stamp = datetime.now()
    t_stamp = str(t_stamp)
    t_stamp = t_stamp.replace('-','')
    t_stamp = t_stamp.replace(' ', '')
    t_stamp = t_stamp.replace(':', '')

    #don't need fractional seconds for this
    return t_stamp.split('.')[0]


if __name__ == '__main__':

    img_input_path = '../data/xeno-canto/img_data/'


    '''
    creat function to read all the files from the input directory
    create % train test split
    process features as decided
    output images to directories for imagedatagenerator to use
    '''
    #get input genorator to images
    train_datagen = ImageDataGenerator(rescale=1./255)
    train_validation_datagen = ImageDataGenerator(rescale=1./255)
    X_train_gen = train_datagen.flow_from_directory(img_input_path + 'train/',
                    class_mode='categorical',
                    target_size=(xpixels,ypixels),
                    color_mode='grayscale',
                    shuffle=True)
    X_test_gen = train_validation_datagen.flow_from_directory(img_input_path + 'validation/',
                    class_mode='categorical',
                    target_size=(xpixels,ypixels),
                    color_mode='grayscale',
                    shuffle=True)

    model = bird_model(X_train_gen.num_class)

    t_stamp = get_time_str()

    #use tensorboard to see output and tweak
    data_run_name = 'imgdata_33k_big2dcnn_stft'+t_stamp
    tensorbd = TensorBoard('logs/' + data_run_name)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit_generator(
        X_train_gen,
        verbose=1,
        steps_per_epoch=15, #300 should typically be equal to the number of unique samples of your dataset divided by the batch size
        epochs=6,  #50,
        callbacks=[tensorbd],
        validation_data=X_test_gen,
        validation_steps=100) # validation_steps should be equal to
                             # the number of unique samples of your
                             # VALIDATION dataset divided by the batch size.

    #saving weights and model both just to be pedantic
    weight_file = data_run_name + t_stamp + '.weights'
    model.save_weights(weight_file)

    model_file = data_run_name + t_stamp + '_model.hdf5'
    model.save(model_file)

    '''
    FYI:
    model.save_weights(filepath): saves the weights of the model as a HDF5 file.
    model.load_weights(filepath, by_name=False): loads the weights of the model
    from a HDF5 file (created by  save_weights). By default, the architecture is
    expected to be unchanged. To load weights into a different
    architecture (with some layers in common), use by_name=True to load only
    those layers with the same name.
    '''

    #make predictions
    # for all of validation set
    # for a one off entered in to show misclassification


    #using my validation items make a prediction with the labels and return
    # do for all then do for one
