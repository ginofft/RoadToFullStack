import torch
from types import SimpleNamespace
from pathlib import Path
import cv2

class ImageDataset1(torch.utils.data.Dataset):
  """This class handle data loading - Pytorch style
  """
  default_conf = {
      'globs': ['*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG'],
      'grayscale': False,
      'interpolation': 'cv2_area'
  }
  def __init__(self, root, conf, paths = None):
    """This function read and save paths of a folder of images
    """
    self.conf = conf = SimpleNamespace(**{**self.default_conf, **conf})
    self.root = root
    paths = []
    for g in conf.globs:
      paths += list(Path(root).glob('**/'+g))
    if len(paths) == 0:
      raise ValueError(f'Could not find any image in root: {root}.')
    paths = sorted(list(set(paths)))
    self.names = [i.relative_to(root).as_posix() for i in paths]
  
  def __getitem__(self, idx):
    """This function is used to load specific item from ImageDataset.
    The load is performed only when specific idx is called -> saving RAM
    """
    name = self.names[idx]
    image = read_image(self.root/name)
    size = image.shape[:2][::-1]
    feature = compute_SIFT(image)
    data = {
        'image': image,
        'feature': feature
    }
    return data
  def __len__(self):
    return len(self.names)
  
class ImageDataset(torch.utils.data.Dataset):
  default_conf = {
    'globs': ['*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG'],
    'grayscale': False,
    'interpolation': 'cv2_area'
  }
  def __init__(self, root):
    self.root = root
    self.names = []
    for g in self.default_conf['globs']:
      self.names += list(Path(root).glob('**/'+g))
    if len(self.names) == 0:
      raise ValueError(f'Could not find any image in root: {root}.')
    self.names = [i.relative_to(self.root).as_posfix() for i in self.names]
  
  def __getitem__(self, idx):
    image = _read_image(self.root/self.names[idx])
    return image

  def __len__(self):
    return len(self.names)

  def _read_image(self, path):
    image = cv2.imread(str(path))
    if self.default_conf['grayscale']:
      image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

