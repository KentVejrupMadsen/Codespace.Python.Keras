from keras \
    import layers, Input, Model

from keras.layers \
    import Rescaling

from keras.utils \
    import image_dataset_from_directory

from tensorflow.python.keras.callbacks \
    import \
    EarlyStopping, \
    ModelCheckpoint

from custom.configuration.global_entries \
    import \
    get_epochs, \
    get_batch_size, \
    get_image_width, \
    get_image_height, \
    get_validation_split, \
    get_preserve_aspect, \
    get_max_classes, \
    get_model_name, \
    get_seed, \
    get_image_color_mode, \
    get_image_color_channels


class CustomModel:
    def __init__(
            self,
            input_node: tuple = (
                    get_image_width(),
                    get_image_height(),
                    get_image_color_channels()
            ),
            batch_size: int = get_batch_size(),

            model_size_width: int = 5,
            model_size_height: int = 128,

            max_classes: int = get_max_classes(),

            image_width: int = get_image_width(),
            image_height: int = get_image_height(),

            color_mode: str = get_image_color_mode(),
            preserve_aspect: bool = get_preserve_aspect(),

            seed: int = get_seed(),
            split_dataset_for_validation: int = get_validation_split(),
            kernel_value: tuple = (3, 3),
            color_channels: int = get_image_color_channels()
    ):
        self.kernel = kernel_value

        self.input = Input(
            shape=input_node
        )

        self.output = None
        self.model = None

        self.image_width = image_width
        self.image_height = image_height
        self.image_preserve_aspect = preserve_aspect
        self.image_color_mode = color_mode
        self.color_channels = color_channels

        self.seed = seed
        self.batch_size = batch_size
        self.categories = max_classes

        self.predict = None

        self.split_sample = split_dataset_for_validation

        self.callbacks = []

        self.setup(
            model_size_width,
            model_size_height
        )

    def early_stopper_added(self):
        callbacks = self.callbacks
        early_stopping = EarlyStopping(
            monitor="loss",
            mode="min",
            verbose=1,
            patience=5
        )

        callbacks.append(
            early_stopping
        )

    def checkpoint_added(self):
        callbacks = self.callbacks

        checkpoint_callback = ModelCheckpoint(
            filepath='/tmp/checkpoint/',
            save_weights_only=False,
            save_best_only=True,
            mode='max',
            monitor='accuracy',
            verbose=0,
            save_freq=4,
            steps_per_execution=50
        )

        callbacks.append(
            checkpoint_callback
        )

    def setup(
            self,
            mid_width_x: int,
            mid_height_y: int
    ):
        start_layer = mid_height_y / 2

        first_layer_in_mid = layers.Conv2D(
            start_layer,
            self.get_kernel(),
            activation='relu',
            input_shape=(
                self.get_image_width(),
                self.get_image_height(),
                self.get_color_channels()
            )
        )

        mid_layers = first_layer_in_mid(
            self.input
        )

        mid_layers = layers.Conv2D(
            mid_height_y,
            self.get_kernel(),
            activation='relu',
            input_shape=(
                self.get_image_width()/2,
                self.get_image_height()/2,
                self.get_color_channels()
            )
        )(mid_layers)

        mid_layers = layers.MaxPooling2D(
            (2, 2)
        )(mid_layers)

        end_pos = mid_width_x - 2

        for idx in range(
                0,
                end_pos
        ):
            mid_layers = layers.Conv2D(
                mid_height_y,
                self.get_kernel(),
                activation='relu'
            )(mid_layers)

        mid_layers = layers.MaxPooling2D(
            (2, 2)
        )(mid_layers)

        self.output = layers.Conv2D(
            mid_height_y,
            self.get_kernel(),
            activation='relu'
        )(mid_layers)

        mid_width_x = layers.Flatten()(self.output)

        prediction = layers.Dense(
            self.get_max_categories(),
            activation='softmax'
        )(mid_width_x)
        self.output = prediction

        self.set_model(
            Model(
                inputs=self.input,
                outputs=self.output,
                name=get_model_name()
            )
        )

        self.model.summary()

    def compile(self):
        self.model.compile(
            loss='SparseCategoricalCrossentropy',
            optimizer='adam',
            metrics=[
                "accuracy"
            ]
        )

    def image_size(self):
        return (
            self.get_image_width(),
            self.get_image_height()
        )

    def fit(
            self,
            path_to_dataset: str
    ):
        training = image_dataset_from_directory(
            path_to_dataset,
            color_mode=self.get_image_color_mode(),
            batch_size=self.get_batch_size(),

            shuffle=True,

            crop_to_aspect_ratio=self.get_image_preserve_aspect(),
            image_size=self.image_size(),

            subset='training',

            validation_split=self.get_validation_split(),
            seed=self.get_seed()
        )

        validation = image_dataset_from_directory(
            path_to_dataset,
            color_mode=self.get_image_color_mode(),
            batch_size=self.get_batch_size(),
            shuffle=True,

            crop_to_aspect_ratio=self.get_image_preserve_aspect(),
            image_size=self.image_size(),

            subset='validation',

            validation_split=self.get_validation_split(),
            seed=self.get_seed()
        )

        Rescaling(1. / 255)

        history = self.get_model().fit(
            training,

            validation_data=validation,

            epochs=get_epochs(),

            callbacks=self.get_callbacks(),

            shuffle=True,

            validation_freq=250
        )

    def get_model(self) -> Model:
        return self.model

    def set_model(self, value: Model):
        self.model = value

    def get_callbacks(self) -> list:
        return self.callbacks

    def set_image_size(
            self,
            width: int,
            height: int
    ):
        self.image_width = width
        self.image_height = height

    def get_image_width(self) -> int:
        return self.image_width

    def get_image_height(self) -> int:
        return self.image_height

    def get_color_channels(self):
        return self.color_channels

    def get_max_categories(self):
        return self.categories

    def get_kernel(self):
        return self.kernel

    def get_batch_size(self):
        return self.batch_size

    def get_seed(self) -> int:
        return self.seed

    def get_validation_split(self) -> float:
        return self.split_sample

    def get_image_preserve_aspect(self):
        return self.image_preserve_aspect

    def get_image_color_mode(self) -> str:
        return self.image_color_mode
