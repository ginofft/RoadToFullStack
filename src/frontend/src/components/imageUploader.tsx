import React, { useState } from "react"
import './imageUploader.css'

function ImageUploader(){
    const [selectedImage, setSelectedImage] = useState<File | null>(null)
    const [uploadedImages, setUploadedImages] = useState([])

    function hanldeImageUpload(event){
        const file = event.target.files[0]
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onloadend = () => {
            setUploadedImages([...uploadedImages, reader.result])
        }
    }

    function handleImageClick(image){
        setSelectedImage(image)
    }

    return (
        <div className="image-uploader">
            <div className='selected-image'>
                {selectedImage ? (
                    <img src={selectedImage} alt="selected" height="300px"/>
                ) : (   
                    <p>No Image Selected</p>
                )
            }
            </div>
            <div className="image-list">
                <input
                    type="file"
                    accept="image/*"
                    onChange={hanldeImageUpload}
                />
                <ul>
                    {uploadedImages.map((image) => (    
                        <li key={image} onClick={() => handleImageClick(image)}>
                            <img src={image} alt="uploaded" height="50px"/>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    )
}

export default ImageUploader;
