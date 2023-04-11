import React, { useState } from "react";
import "./imageUploader.css";
import axios from 'axios';

const url = 'http://localhost:8000/api/upload'

function imageUploader() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [uploadedImages, setUploadedImages] = useState<string[]>([]);

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
    console.log(imageId)
    try{
      const response = await axios.post(url, {imageId});
      console.log(response.data)
    } catch (error){
      console.error(error)
    }
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
    </div>
  );
}

export default imageUploader;
