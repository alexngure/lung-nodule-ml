import flatbuffers
import TrainingData.Example as FBExample
import TrainingData.Header as FBHeader
import TrainingData.TrainingSet as FBTrainingSet
import numpy as np
from Utils import get_image

class DataLoader(object):
    """A class to facilitate data loading during training and testing."""
    def __init__(self, path, train_percent = 0.8):
        self.path = ''
        self.test_images = ''
        self.test_labels = ''
        self.train_percent = train_percent
        self.test_percent = 1 - train_percent
    def load_data(self,src=self.path):
        """Load data file via the path specified at object initialization
        or 'src'
        """
        return

    def next_batch(self,batch_size):
        """Return a minibatch of the specified size from
        the loaded dataset.
        """
        return

class DataCreator(object):
    """A class to convert raw data into its representational state (ex.
    a raw image into a 2D matrix of floats), and write it to disk in a
    convenient format.
    """
    def __init__(self,src,dest):
        self.src = src
        self.dest = dest
        self.num_examples = 0
        self.builder = flatbuffer.Builder(0)
        self.examples = []
    def add_example(self,src):
        """Takes DICOM file 'src' and extracts its pixel data, and flattens
        its into a vector to create a training example.
        """
        im = get_image(src)
        im_array = np.array(im).flatten()
        return

    def add_examples(self,src):
        """Converts all the DICOM images in directory 'src' into
        training examples.
        """
        return

    def write_file(self,dest):
        """Writes out a '.data' file containing all the examples
         added so far.
         """
        return
