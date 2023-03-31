from pathlib import Path
from typing import Optional

from sklearn.cluster import KMeans
from joblib import dump, load
import numpy as np
import cv2

from .dataset import ImageDataset
class vlad:
  '''This class is used to find visual vocabularies of a dataset; From which, calculation of VLAD of a dataset (or image) can be done

  Attributes
  ----------
  `vocabs` : numpy.ndarray
    visual vocabularies of a dataset
  `kmeans` : sklearn.cluster.KMeans
    Kmeans object used to find visual vocabularies and calculate VLAD

  Methods
  -------
  `find_cluster(dataset, no_vocab)` -> None
    find visual vocabularies of a dataset, update `self.vocabs` and `self.kmeans`
  `save_cluster(path)` -> None
    save `self.kmeans` into `path`
  `load_cluster(path)` -> None
    load `self.kmeans` from `path`
  `save_dataset_vlad(dataset, out_path)` -> npdarray
    calculate VLAD of a dataset and save it into `out_path` and return it
  '''
  _sift = cv2.SIFT_create()
  def __init__(self, path: Optional[Path] = None):
    self.kmeans = None
    if path is not None:
      self.load_cluster(path)

  @property
  def vocabs(self):
      return self.kmeans.cluster_centers_

  def find_cluster(self, dataset: ImageDataset, no_vocab: int) -> None: 
    dataset_descriptors = []
    for image in dataset:
      sift_descriptor = self._calculate_SIFT(image)
      dataset_descriptors.append(sift_descriptor)
    
    dataset_descriptors = np.concatenate(dataset_descriptors, axis=0)    
    self.kmeans = KMeans(n_clusters=no_vocab, n_init='auto').fit(dataset_descriptors)

  def save_cluster(self, path = './output/cluster.joblib'):
    dump(self.kmeans, path)

  def load_cluster(self, path = './output/cluster.joblib'):
    self.kmeans = load(path)

  def save_dataset_vlad(self,
                        dataset: ImageDataset,
                        out_path = './output/vlads.npy') -> np.ndarray:
    vlads = np.zeros([len(dataset), self.vocabs.shape[0]*self.vocabs.shape[1]])
    for i, image in enumerate(dataset):
      vlads[i] = self.calculate_VLAD(image)
    np.save(out_path, vlads)
    return vlads 
    
  def _calculate_SIFT(self, image):
    _, des = self._sift.detectAndCompute(image, None)
    return des
  
  def calculate_VLAD(self, image) -> np.ndarray:
    if self.kmeans == None:
      raise Exception('Vocaburaly not found, please run find_cluster() or load_cluster() first')
    
    sift_descriptor = self._calculate_SIFT(image)
    nn = self.kmeans.predict(sift_descriptor)
    vlad = np.zeros(self.vocabs.shape)

    for i in range(self.vocabs.shape[0]):
      vlad[i] = np.sum(sift_descriptor[nn==i] - self.vocabs[i], axis=0)
    
    vlad = vlad.flatten()
    #vlad = np.sign(vlad)*np.sqrt(np.abs(vlad)) #power norm ??
    vlad = vlad/np.sqrt(np.dot(vlad,vlad))        #L2 norm
    
    return vlad