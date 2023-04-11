import React, { useState } from "react";
import "./imageUploader.css";
import axios from 'axios';
import header from "./header";

const url = 'http://localhost:8000/queryImage'

function imageUploader() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [uploadedImages, setUploadedImages] = useState<string[]>([]);
  const [retrievedImages, setRetrievedImages] = useState<{ name: string, image: string }[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');

  function handleImageUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files ? event.target.files[0] : null;
    if (file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onloadend = () => {
        setUploadedImages([...uploadedImages, reader.result as string]);
      };
    }
  }

  const handleImageClick = async (imageId: string) => {
    setSelectedImage(imageId)
    const blob = await (await fetch(imageId)).blob()
    const formData = new FormData()
    formData.append('imageFile', blob)
    setIsLoading(true);
    setErrorMessage('');
    try {
      const response = await axios.post(url, formData, {
        headers: {
          "Content-type": "multipart/form-data",
        }
      })
      if (response.data.status === "ok") {
        setRetrievedImages(response.data.results);
      } else {
        setErrorMessage("Failed to retrieve images.");
      }
    }
    catch (error) {
      setErrorMessage("Failed to retrieve images.");
    }
    setIsLoading(false);
  }

  return (
    <div className="image-uploader">
      <div className="selected-image">
        {selectedImage ? (
          <img src={selectedImage} alt="selected" />
        ) : (
          <p>No Image Selected</p>
        )}
      </div>
      <div className="image-list-wrapper">
        <div className="image-list">
          <ul>
            {uploadedImages.map((image) => (
              <li key={image} onClick={() => handleImageClick(image)}>
                <img src={image} alt="uploaded" />
              </li>
            ))}
          </ul>
        </div>
        <div className="upload-btn">
          <label htmlFor="file-input">Choose File</label>
          <input
            id="file-input"
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
          />
        </div>
      </div>
      <div className="retrieved-image-container">
        {retrievedImages.map((image) => (
          <div key={image.name} className="retrieved-image">
            <img src={`data:image/png;base64,${image.image}`} alt={image.name} />
          </div>
        ))}
      </div>
    </div>
  );  
}

export default imageUploader;