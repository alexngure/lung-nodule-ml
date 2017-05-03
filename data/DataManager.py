
import TrainingData.Example as FBExample
import TrainingData.Header as FBHeader
import TrainingData.TrainingSet as FBTrainingSet

class DataLoader(object):
    """A class to facilitate data loading during training and testing."""
    def __init__(self, path, train_percent = 0.8):
        self.path = ''
        self.test_images = ''
        self.test_labels = ''
        self.train_percent = train_percent
        self.test_percent = 1 - train_percent
    def load_data(self):
        return
    def next_batch(self,batch_size):
        return

class DataCreator(object):
    """A class to convert raw data into its representational state (ex.
    a raw image into a 2D matrix of floats), and write it to disk in a
    convenient format."""
    def __init__(self,src,dest):
        self.src = src
        self.dest = dest
