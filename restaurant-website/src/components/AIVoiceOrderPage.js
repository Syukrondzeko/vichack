import React, { useState } from 'react';
import Header from './Header';
import './AIVoiceOrderPage.css';

const AIVoiceOrderPage = ({ onBack }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [recognition, setRecognition] = useState(null);

  const startRecording = () => {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      alert('Your browser does not support speech recognition.');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = true;
    recognitionInstance.interimResults = true;
    recognitionInstance.lang = 'en-US';

    recognitionInstance.onstart = () => {
      setIsRecording(true);
      setTranscript(''); // Clear transcript when starting a new recording
    };

    recognitionInstance.onresult = (event) => {
      let finalTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        }
      }
      setTranscript(finalTranscript);
    };

    recognitionInstance.onend = () => {
      setIsRecording(false);
    };

    recognitionInstance.onerror = (event) => {
      console.error('Speech recognition error detected: ' + event.error);
    };

    recognitionInstance.start();
    setRecognition(recognitionInstance);
  };

  const stopRecording = () => {
    if (recognition) {
      recognition.stop();
    }
  };

  return (
    <div>
      <Header showNavLinks={false} />
      <div className="ai-voice-order-container text-center">
        <h2>AI Voice Order</h2>
        <p>Press the button below to begin recording your order.</p>
        <div>
          <div className="transcript">
            <p>{transcript}</p> {/* Show the final transcript */}
          </div>
          <div className="btn-container">
            {!isRecording ? (
              <button onClick={startRecording} className="btn btn-primary mt-3">
                Begin Recording
              </button>
            ) : (
              <button onClick={stopRecording} className="btn btn-danger mt-3">
                Stop Recording
              </button>
            )}
          </div>
        </div>
        <button onClick={onBack} className="btn btn-secondary mt-3">
          Back to Main Menu
        </button>
      </div>
    </div>
  );
};

export default AIVoiceOrderPage;
