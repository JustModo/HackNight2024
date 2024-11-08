// // src/components/CaptureScreenshot.jsx
// import React, { useState } from 'react';
// import html2canvas from 'html2canvas';
// import '../styles/CaptureScreenshot.css';

// const CaptureScreenshot = () => {
//   const [screenshot, setScreenshot] = useState(null);

//   const takeScreenshot = () => {
//     html2canvas(document.body).then((canvas) => {
//       const imgData = canvas.toDataURL('image/png');
//       setScreenshot(imgData);
//     });
//   };

//   const removeScreenshot = () => {
//     setScreenshot(null);
//   };

//   return (
//     <div className="capture-screenshot-container">
//       <button onClick={takeScreenshot} className="capture-screenshot-button">
//         Take Screenshot
//       </button>

//       {screenshot && (
//         <div className="screenshot-preview">
//           <img src={screenshot} alt="Screenshot" className="captured-screenshot" />
//           <button onClick={removeScreenshot} className="remove-screenshot-button">
//             Remove Screenshot
//           </button>
//         </div>
//       )}
//     </div>
//   );
// };

// export default CaptureScreenshot;
