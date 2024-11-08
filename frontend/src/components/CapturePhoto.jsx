// // src/components/CapturePhoto.jsx
// import React, { useRef, useCallback, useState } from 'react';
// import Webcam from 'react-webcam';
// import '../styles/CapturePhoto.css';

// const CapturePhoto = () => {
//   const webcamRef = useRef(null);
//   const [photo, setPhoto] = useState(null);

//   const capture = useCallback(() => {
//     const imageSrc = webcamRef.current.getScreenshot();
//     setPhoto(imageSrc);
//   }, [webcamRef]);

//   return (
//     <div className="capture-photo-container">
//       <Webcam
//         audio={false}
//         ref={webcamRef}
//         screenshotFormat="image/jpeg"
//         videoConstraints={{
//           facingMode: "user",
//         }}
//         style={{
//           width: '100%',  // Ensures webcam fills the container
//           height: 'auto',
//           borderRadius: '12px',
//         }}
//       />
//       <button onClick={capture} className="capture-photo-button">Take Photo</button>
//       {photo && <img src={photo} alt="Captured" className="captured-photo" />}
//     </div>
//   );
// };

// export default CapturePhoto;
