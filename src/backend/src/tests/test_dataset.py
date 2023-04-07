from ..dataset import ImageDataset

dataset = ImageDataset('src/backend/database')

def test_init() -> None:
    """Test the initialization of the ImageDataset class
    """
    assert len(dataset) == 1019

def test_getitem() -> None:
    """Test the __getitem__ function of the ImageDataset class
    """
    assert len(dataset[0].shape) == 3
    assert len(dataset[1].shape) == 3
