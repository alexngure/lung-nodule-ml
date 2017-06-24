import random
import flatbuffers
import LungData.Dataset as FBDataset
import TrainingData.Example as FBExample
import TrainingData.Header as FBHeader
import TrainingData.TrainingSet as FBTrainingSet
import numpy as np
from Utils import get_image,Nodule

class DataLoader(object):
    """A class to facilitate data loading during training and testing."""
    def __init__(self, positive_path, negative_path, train_percent = 0.8):
        self.test_images = ''
        self.test_labels = ''
        self.train_percent = train_percent
        self.test_percent = 1 - train_percent

        self.positive_path = positive_path
        self.positive_cases = []
        for (path,dirs,files) in os.walk(positive_path):
            self.positive_cases.extend(files)
            break

        self.negative_path = negative_path
        self.negative_cases = []
        for (path,dirs,files) in os.walk(negative_path):
            self.negative_cases.extend(files)
            break

        self.n_positive = int(len(self.positive_cases)*train_percent)
        self.n_negative = int(len(self.negative_cases)*train_percent)

    def next_batch(self,batch_size):
        """Return a minibatch of the specified size from
        the loaded dataset.
        """
        num_cases = int(batch_size/2)
        examples = []
        labels   = []
        random.seed()
        for i in range(0,num_cases):
            pos_idx     = random.randint(0,self.n_positive)
            neg_idx     = random.randint(0,self.n_negative)
            pos_path    = os.path.join(self.positive_path, self.positive_cases[pos_idx])
            neg_path    = os.path.join(self.negative_path, self.negative_cases[neg_idx])
            examples.append(load_image(pos_path))
            labels.append([1,0])
            examples.append(load_image(neg_path))
            labels.append([0,1])
        examples = np.stack(examples)
        labels   = np.stack(labels)
        return examples,labels

    def test_examples(self):
        """Returns the examples reserved for testing."""
        examples = []
        labels   = []
        for i in range(self.n_positive,len(self.positive_cases)-1):
            pos_path = os.path.join(self.positive_path, self.positive_cases[i])
            examples.append(load_image(pos_path))
            labels.append([1,0])
        for i in range(self.n_negative,len(self.negative_cases)-1):
            neg_path = os.path.join(self.negative_path, self.negative_cases[i])
            examples.append(load_image(neg_path))
            labels.append([0,1])
        examples = np.stack(examples)
        labels   = np.stack(labels)
        return examples,labels

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

class DataBuffer(object):
    """A class that provides convenient accessors into a .lng data
    buffer.
    """
    def __init__(self,src,instance_map):
        self.src = src
        self.dataset = read_lng(src)
        self.size = len(self.dataset)
        self.instance_map = instance_map

    def read_lng(self,src):
        """Reads .lng file src and returns a dictionary object of
        (nodule_ID,Utils.Nodule) key-value pairs.
        """
        buf = open(src,'rb').read()
        buf = bytearray(buf)
        dataset_buf = FBDataset.GetRootAsDataset(buf,0)
        dataset = {}
        for i in range(0,dataset_buf.DataLength()):
            fb_nodule = dataset_buf.Data(i)
            dataset[fb_nodule.NoduleId()] = fb_nodule
        return dataset

    def get_nodule(self,nodule_ID):
        """Returns a LungData.Nodule object for nodule with the specified
        nodule_ID.
        """
        try:
            return dataset[nodule_ID]
        except:
            return None

    def show_nodule(self,nodule_ID,outlined=True,filled=True):
        """Displays the DICOM instance containing the nodule with the specified
        ID as a png image.
        """
        return

    def print_nodule(self,nodule_ID,dest,outlined=False,filled=False):
        """Outputs the DICOM instance containing the nodule with the specified ID
        as a png image in dest.
        """
        nodule = self.dataset[nodule_ID]
        return

    def get_image(self,nodule_ID):
        """Returns a PIL image object for the DICOM instance containing
        nodule with the specified ID.
        """
        return

    def get_dcm(self,nodule_ID):
        """Returns a pydicom DICOM object for the instance containing nodule
        with the specified nodule_ID.
        """
        return

    def size(self):
        """Returns the total number of nodules in this DataBuffer."""
        return self.size
