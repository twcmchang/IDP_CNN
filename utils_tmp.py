#######################################################################
#
# Functions for downloading the CIFAR-10 data-set from the internet
# and loading it into memory.
#
# Implemented in Python 3.5
#
# Usage:
# 1) Set the variable data_path with the desired storage path.
# 2) Call maybe_download_and_extract() to download the data-set
#    if it is not already located in the given data_path.
# 3) Call load_class_names() to get an array of the class-names.
# 4) Call load_training_data() and load_test_data() to get
#    the images, class-numbers and one-hot encoded class-labels
#    for the training-set and test-set.
# 5) Use the returned data in your own program.
#
# Format:
# The images for the training- and test-sets are returned as 4-dim numpy
# arrays each with the shape: [image_number, height, width, channel]
# where the individual pixels are floats between 0.0 and 1.0.
#
########################################################################
#
# This file is part of the TensorFlow Tutorials available at:
#
# https://github.com/Hvass-Labs/TensorFlow-Tutorials
#
# Published under the MIT License. See the file LICENSE for details.
#
# Copyright 2016 by Magnus Erik Hvass Pedersen
#
########################################################################
import os
import pickle
import numpy as np

class CIFAR10(object):
    def __init__(self):

        ########################################################################
        # Directory where you want to download and save the data-set.
        # Set this before you start calling any of the functions below.
        self.data_path = "/data/put_data/cmchang/"

        # base folder
        self.base_folder = "cifar-10-batches-py/"

        # URL for the data-set on the internet.
        self.data_url = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"

        ########################################################################
        # Various constants for the size of the images.
        # Use these constants in your own program.

        # Width and height of each image.
        self.img_size = 32

        # Number of channels in each image, 3 channels: Red, Green, Blue.
        self.num_channels = 3

        # Length of an image when flattened to a 1-dim array.
        self.img_size_flat = self.img_size * self.img_size * self.num_channels

        # Number of classes.
        self.num_classes = 10

        ########################################################################

    def _one_hot_encoded(self, class_numbers, num_classes=None):
        """
        Generate the One-Hot encoded class-labels from an array of integers.
        For example, if class_number=2 and num_classes=4 then
        the one-hot encoded label is the float array: [0. 0. 1. 0.]
        :param class_numbers:
            Array of integers with class-numbers.
            Assume the integers are from zero to num_classes-1 inclusive.
        :param num_classes:
            Number of classes. If None then use max(class_numbers)+1.
        :return:
            2-dim array of shape: [len(class_numbers), num_classes]
        """

        # Find the number of classes if None is provided.
        # Assumes the lowest class-number is zero.
        if num_classes is None:
            num_classes = np.max(class_numbers) + 1

        return np.eye(num_classes, dtype=float)[class_numbers]

    ########################################################################
    # Private functions for downloading, unpacking and loading data-files.

    def _unpickle(self, filename):
        """
        Unpickle the given file and return the data.

        Note that the appropriate dir-name is prepended the filename.
        """

        # Create full path for the file.
        file_path = os.path.join(self.data_path, self.base_folder, filename)

        print("Loading data: " + file_path)

        with open(file_path, mode='rb') as file:
            # In Python 3.X it is important to set the encoding,
            # otherwise an exception is raised here.
            data = pickle.load(file, encoding='bytes')

        return data


    def _convert_images(self, raw):
        """
        Convert images from the CIFAR-10 format and
        return a 4-dim array with shape: [image_number, height, width, channel]
        where the pixels are floats between 0.0 and 1.0.
        """

        # Convert the raw images from the data-files to floating-points.
        raw_float = np.array(raw, dtype=float) / 255.0

        # Reshape the array to 4-dimensions.
        images = raw_float.reshape([-1, self.num_channels, self.img_size, self.img_size])

        # Reorder the indices of the array.
        images = images.transpose([0, 2, 3, 1])

        return images


    def _load_data(self, filename):
        """
        Load a pickled data-file from the CIFAR-10 data-set
        and return the converted images (see above) and the class-number
        for each image.
        """

        # Load the pickled data-file.
        data = self._unpickle(filename)

        # Get the raw images.
        raw_images = data[b'data']

        # Get the class-numbers for each image. Convert to numpy-array.
        cls = np.array(data[b'labels'])

        # Convert the images.
        images = self._convert_images(raw_images)

        return images, cls

    ########################################################################
    # Public functions that you may call to download the data-set from
    # the internet and load the data into memory.

    def load_class_names(self):
        """
        Load the names for the classes in the CIFAR-10 data-set.

        Returns a list with the names. Example: names[3] is the name
        associated with class-number 3.
        """

        # Load the class-names from the pickled file.
        raw = _unpickle(filename="batches.meta")[b'label_names']

        # Convert from binary strings.
        names = [x.decode('utf-8') for x in raw]

        return names


    def load_training_data(self):
        """
        Load all the training-data for the CIFAR-10 data-set.

        The data-set is split into 5 data-files which are merged here.

        Returns the images, class-numbers and one-hot encoded class-labels.
        """
        # Number of files for the training-set.
        _num_files_train = 5

        # Number of images for each batch-file in the training-set.
        _images_per_file = 10000

        # Total number of images in the training-set.
        # This is used to pre-allocate arrays for efficiency.
        _num_images_train = _num_files_train * _images_per_file
        
        
        # Pre-allocate the arrays for the images and class-numbers for efficiency.
        images = np.zeros(shape=[_num_images_train, self.img_size, self.img_size, self.num_channels], dtype=float)
        cls = np.zeros(shape=[_num_images_train], dtype=int)

        # Begin-index for the current batch.
        begin = 0

        # For each data-file.
        for i in range(_num_files_train):
            # Load the images and class-numbers from the data-file.
            images_batch, cls_batch = self._load_data(filename="data_batch_" + str(i + 1))

            # Number of images in this batch.
            num_images = len(images_batch)

            # End-index for the current batch.
            end = begin + num_images

            # Store the images into the array.
            images[begin:end, :] = images_batch

            # Store the class-numbers into the array.
            cls[begin:end] = cls_batch

            # The begin-index for the next batch is the current end-index.
            begin = end

        return images, self._one_hot_encoded(class_numbers=cls, num_classes=self.num_classes)


    def load_test_data(self):
        """
        Load all the test-data for the CIFAR-10 data-set.

        Returns the images, class-numbers and one-hot encoded class-labels.
        """

        images, cls = self._load_data(filename="test_batch")

        return images, self._one_hot_encoded(class_numbers=cls, num_classes=self.num_classes)

    ########################################################################

    ########################################################################
    #
    # Functions for downloading and extracting data-files from the internet.
    #
    # Implemented in Python 3.5
    #
    ########################################################################
    #
    # This file is part of the TensorFlow Tutorials available at:
    #
    # https://github.com/Hvass-Labs/TensorFlow-Tutorials
    #
    # Published under the MIT License. See the file LICENSE for details.
    #
    # Copyright 2016 by Magnus Erik Hvass Pedersen
    #
    ########################################################################

    import sys
    import os
    import urllib.request
    import tarfile
    import zipfile

    ########################################################################


    def _print_download_progress(self, count, block_size, total_size):
        """
        Function used for printing the download progress.
        Used as a call-back function in maybe_download_and_extract().
        """

        # Percentage completion.
        pct_complete = float(count * block_size) / total_size

        # Status-message. Note the \r which means the line should overwrite itself.
        msg = "\r- Download progress: {0:.1%}".format(pct_complete)

        # Print it.
        sys.stdout.write(msg)
        sys.stdout.flush()


    ########################################################################


    def maybe_download_and_extract(self, url, download_dir):
        """
        Download and extract the data if it doesn't already exist.
        Assumes the url is a tar-ball file.
        :param url:
            Internet URL for the tar-file to download.
            Example: "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
        :param download_dir:
            Directory where the downloaded file is saved.
            Example: "data/CIFAR-10/"
        :return:
            Nothing.
        """

        # Filename for saving the file downloaded from the internet.
        # Use the filename from the URL and add it to the download_dir.
        filename = url.split('/')[-1]
        file_path = os.path.join(download_dir, filename)

        # Check if the file already exists.
        # If it exists then we assume it has also been extracted,
        # otherwise we need to download and extract it now.
        if not os.path.exists(file_path):
            # Check if the download directory exists, otherwise create it.
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # Download the file from the internet.
            file_path, _ = urllib.request.urlretrieve(url=url,
                                                      filename=file_path,
                                                      reporthook=self._print_download_progress)

            print()
            print("Download finished. Extracting files.")

            if file_path.endswith(".zip"):
                # Unpack the zip-file.
                zipfile.ZipFile(file=file_path, mode="r").extractall(download_dir)
            elif file_path.endswith((".tar.gz", ".tgz")):
                # Unpack the tar-ball.
                tarfile.open(name=file_path, mode="r:gz").extractall(download_dir)

            print("Done.")
        else:
            print("Data has apparently already been downloaded and unpacked.")

    ########################################################################

