import React, { useState } from "react";
import "./imageUploader.css";
import axios from 'axios';
import header from "./header";

const url = 'http://localhost:8000/queryImage'

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
    const blob = await (await fetch(imageId)).blob()
    const formData = new FormData()
    formData.append('imageFile', blob)
    const response = await axios.post(url, formData,
      {
        headers: {
          "Content-type": "multipart/form-data",
        }
      }
    )
    console.log(response.data)
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

function DataURIToBlob(dataURI: string)
{
  const splitDataURI = dataURI.split(',')
  const byteString = splitDataURI[0].indexOf('base64') > 0 ? atob(splitDataURI[1]) : decodeURI(splitDataURI[1])
  const mimeString = splitDataURI[0].split(':')[1].split(';')[0]

  const ia  = new Uint8Array(byteString.length)
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i)
  }
  return new Blob([ia], {type: mimeString})
}
export default imageUploader;