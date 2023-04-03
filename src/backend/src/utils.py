import numpy as np
import cv2

def read_image(path, grayscale=False):
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

def get_topk_indices(db_vlad, q_vlad,k) -> np.ndarray:
    '''This function is used to find the indices of top k most similar database images from a query image

    Parameters
    ----------
    `db_vlad` : numpy.ndarray
        VLAD of a database
    `q_vlad` : numpy.ndarray
        VLAD of a query image
    `k` : int
        number of top images to be found

    Returns
    -------
    `retrieved_indices` : numpy.ndarray
        shape = [q_vlad.shape[0], k] contains the indices of top k most similar database images from a query image
    '''
    
    if q_vlad.ndim == 1:
        q_vlad = q_vlad[np.newaxis, :]

    # similarity [i, j] corresponds to the similarity between the i-th query image and the j-th database image
    similarity = q_vlad @ db_vlad.T # shape: (q_vlad.shape[0], db_vlad.shape[0])  
    
    retrieved_indices = np.zeros([q_vlad.shape[0], k], dtype=np.int32)
    for i in range(similarity.shape[0]):
        topk_indices = np.argsort(similarity[i, :])[-k:][::-1]
        retrieved_indices[i, :] = topk_indices
    
    return retrieved_indices

