from keras.preprocessing.image \
    import ImageDataGenerator

from configuration.path_configuration import \
    get_train_path, \
    get_validation_path, \
    get_test_path

from configuration.machine_state \
    import \
    get_default_image_size, \
    get_normalise_value, \
    get_batch_size_value

from os.path \
    import join

from os \
    import walk

import cv2

import numpy as np


class LoadDataset:
    def __init__(
            self,
            train: str,
            validate: str,
            test: str
    ):
        self.train_path = train
        self.validation_path = validate
        self.test_path = test

    def load_train_path(self) -> str:
        return self.train_path

    def load_validation_path(self) -> str:
        return self.validation_path

    def load_test_path(self) -> str:
        return self.test_path

    def load_train_set(self) -> list:
        r_values = []

        for root_directory, \
            directories, \
            files \
                in walk(self.train_path):
            for file \
                    in files:
                full_path = join(
                    root_directory,
                    file
                )

                image_array = cv2.imread(
                    full_path
                )

                image_array = cv2.resize(
                    image_array,
                    get_default_image_size()
                )

                r_values.append(
                    image_array
                )

        return r_values

    def load_test_set(self):
        r_values = []

        for \
                root_directory, \
                directories, \
                files \
                in walk(self.test_path):
            for file \
                    in files:
                full_path = join(
                    root_directory,
                    file
                )

                image_array = cv2.imread(
                    full_path
                )

                image_array = cv2.resize(
                    image_array,
                    get_default_image_size()
                )

                r_values.append(
                    image_array
                )

        return r_values

    def load_validation_set(self):
        r_values = []

        for root_directory, \
            directories, \
            files \
                in walk(self.validation_path):

            for file \
                    in files:
                full_path = join(
                    root_directory,
                    file
                )

                image_array = cv2.imread(
                    full_path
                )

                image_array = cv2.resize(
                    image_array,
                    get_default_image_size()
                )

                r_values.append(
                    image_array
                )

        return r_values


def classification() -> dict:
    training_sets = \
    {
        'training': None,
        'train_x': None,

        'test': None,
        'test_x': None,

        'validation': None,
        'validation_x': None
    }

    loaded = LoadDataset(
        get_train_path(),
        get_validation_path(),
        get_test_path()
    )

    dataset_train_x = np.array(
        loaded.load_train_set()
    )

    dataset_train_x = dataset_train_x / get_normalise_value()
    training_sets['train_x'] = dataset_train_x

    training_set_datagen = ImageDataGenerator(
        rescale=1./255
    )

    training_set = training_set_datagen.flow_from_directory(
        loaded.train_path,
        target_size=get_default_image_size(),
        batch_size=get_batch_size_value(),
        class_mode='sparse'
    )
    training_sets['training'] = training_set

    dataset_validation_x = np.array(
        loaded.load_validation_set()
    )
    dataset_validation_x = dataset_validation_x / get_normalise_value()
    training_sets['validation_x'] = dataset_validation_x

    validation_set_datagen = ImageDataGenerator(
        rescale=1./255
    )

    validation_set = validation_set_datagen.flow_from_directory(
        loaded.validation_path,
        target_size=get_default_image_size(),
        class_mode='sparse',
        batch_size=get_batch_size_value()
    )
    training_sets['validation'] = validation_set

    dataset_test_x = np.array(
        loaded.load_test_set()
    )
    dataset_test_x = dataset_test_x / get_normalise_value()
    training_sets['test_x'] = dataset_test_x

    test_set_datagen = ImageDataGenerator(
        rescale=1./255
    )

    test_set = test_set_datagen.flow_from_directory(
        loaded.test_path,
        target_size=get_default_image_size(),
        batch_size=get_batch_size_value(),
        class_mode='sparse'
    )

    training_sets['test'] = test_set

    return training_sets
