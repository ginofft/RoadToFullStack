import React, { useState } from 'react'

const uploadImageField = () => {
    const [selectedImage, setSelectedImage] = useState<File | null>(null)
    return (
        <div>
            <h1>Upload Image</h1>
            {selectedImage&&(
                <div>
                    <img
                        alt='Not Found'
                        width={"250px"}
                        src={URL.createObjectURL(selectedImage)}
                    />
                    <br />
                    <button onClick={()=>setSelectedImage(null)}>Remove</button>
                </div>
            )
            }
            <br />
            <br />
            <input
                type='file'
                name='myImage'
                onChange={(event) => {
                    console.log(event.target.files[0])
                    setSelectedImage(event.target.files[0])
                }}
            />
        </div>
    )
}
            
export default uploadImageField