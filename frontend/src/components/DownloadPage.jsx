// src/components/DownloadPage.jsx
import '../styles/DownloadPage.css';

const DownloadPage = () => {
  return (
    <div className="w-screen h-screen flex flex-col justify-center items-center">
      <div className="download-header flex flex-col items-center">
        <h1>Download the Braille Translator</h1>
        <p>Get the Braille translator app or download useful files below.</p>
      </div>

      <div className="download-links">
        <div className="download-card">
          <h2>Download the Extension</h2>
          <p>Download the Braille Translator Extension on Chrome</p>
          <a className="download-button" onClick={()=>{}}>Download</a>
        </div>
      </div>
    </div>
  );
};

export default DownloadPage;
