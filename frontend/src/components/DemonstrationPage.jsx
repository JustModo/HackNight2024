// src/components/DemonstrationPage.jsx
import { useEffect, useRef, useState } from "react";
import "../styles/DemonstrationPage.css";
import io from "socket.io-client";

// Braille mapping for basic characters
const brailleMapping = {
  a: "⠁",
  b: "⠃",
  c: "⠉",
  d: "⠙",
  e: "⠑",
  f: "⠋",
  g: "⠛",
  h: "⠓",
  i: "⠊",
  j: "⠚",
  k: "⠅",
  l: "⠇",
  m: "⠍",
  n: "⠝",
  o: "⠕",
  p: "⠏",
  q: "⠟",
  r: "⠗",
  s: "⠎",
  t: "⠞",
  u: "⠥",
  v: "⠧",
  w: "⠺",
  x: "⠭",
  y: "⠽",
  z: "⠵",
  0: "⠼⠁",
  1: "⠼⠁",
  2: "⠼⠃",
  3: "⠼⠉",
  4: "⠼⠙",
  5: "⠼⠑",
  6: "⠼⠋",
  7: "⠼⠛",
  8: "⠼⠓",
  9: "⠼⠊",
  ".": "⠲",
  ",": "⠂",
  "?": "⠦",
  "!": "⠖",
  " ": " ",
};

const socket = io("http://localhost:5000");

const DemonstrationPage = () => {
  const [brailleOutput, setBrailleOutput] = useState("");
  const [asciiValues, setAsciiValues] = useState("");

  const prevAsciiValues = useRef("");

  const getMapping = (str) => {
    str = String(str).toLowerCase();
    setAsciiValues(String(str).toUpperCase());
    setBrailleOutput(brailleMapping[str]);
  };

  useEffect(() => {
    socket.on("ocr_result", (char) => {
      getMapping(char);
    });

    socket.emit("start_ocr");

    return () => {
      socket.off("ocr_result");
    };
  }, []);

  useEffect(() => {
    if (asciiValues !== prevAsciiValues.current) {
      const utterance = new SpeechSynthesisUtterance(asciiValues);
      window.speechSynthesis.speak(utterance);

      prevAsciiValues.current = asciiValues;
    }
  }, [asciiValues]); // Only re-run if asciiValues changes

  return (
    <div className="w-screen h-screen flex flex-col items-center p-8 text-white">
      <h1 className="text-4xl font-extrabold py-4 px-12 text-indigo-500 text-center">
        Live Braille Translator
      </h1>

      <div className="flex w-full h-full gap-6 justify-center mt-8">
        <div className="p-6 bg-indigo-500 w-full max-w-4xl text-[7rem] flex justify-around items-center rounded-lg shadow-2xl">
          <div className="text-center">
            <h2 className="text-2xl font-semibold mb-4 opacity-80">
              ASCII Values
            </h2>
            <p className="font-extrabold tracking-wider text-indigo-200">
              {asciiValues}
            </p>
          </div>
          <div className="text-center">
            <h2 className="text-2xl font-semibold mb-4 opacity-80">
              Braille Output
            </h2>
            <p className="font-extrabold tracking-wider text-indigo-200">
              {brailleOutput}
            </p>
          </div>
        </div>
      </div>
      {/* <h1 className="text-4xl font-extrabold py-4 px-12 text-indigo-500 text-center">
        {`Output: ${output}`}
      </h1> */}
    </div>
  );
};

export default DemonstrationPage;
