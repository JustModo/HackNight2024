import React, { useState } from "react";
import "../styles/ImageUpload.css";

const ImageUpload = () => {
  const [photo, setPhoto] = useState(null);

  // Handle file input change
  const handleFileChange = (event) => {
    const file = event.target.files[0]; // Get the selected file
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhoto(reader.result); // Set the uploaded photo as the source
      };
      reader.readAsDataURL(file); // Convert file to base64 string
    }
  };

  return (
    <div className="image-upload-container">
      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="file-input"
      />
      {photo && <img src={photo} alt="Uploaded" className="uploaded-image" />}
    </div>
  );
};

export default ImageUpload;
