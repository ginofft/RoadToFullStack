import torch
from types import SimpleNamespace
from pathlib import Path
import cv2

class ImageDataset(torch.utils.data.Dataset):
  default_conf = {
    'globs': ['*.jpg', '*.png', '*.jpeg'],
    'grayscale': False,
    'interpolation': 'cv2_area'
  }
  def __init__(self, root):
    self.root = Path(root)
    self.names = []
    for g in self.default_conf['globs']:
      self.names += list(Path(root).glob('**/'+g))
    if len(self.names) == 0:
      raise ValueError(f'Could not find any image in root: {root}.')
    self.names = [i.relative_to(self.root).as_posix() for i in self.names]
  
  def __getitem__(self, idx):
    image = self._read_image(self.root/self.names[idx])
    return image

  def __len__(self):
    return len(self.names)
  
  def get_path(self, idx):
    return self.root/self.names[idx]
  
  def _read_image(self, path, grayscale=False):
    """This function read an image from a path.
   
    The read is perform using opencv.
    """
    if grayscale:
        mode = cv2.IMREAD_GRAYSCALE
    else:
        mode = cv2.IMREAD_COLOR
    image = cv2.imread(str(path), mode)
    if image is None:
        raise ValueError(f'Cannot read image {path}.')
    if not grayscale and len(image.shape) == 3:
        image = image[:, :, ::-1]  # BGR to RGB
    return image
  