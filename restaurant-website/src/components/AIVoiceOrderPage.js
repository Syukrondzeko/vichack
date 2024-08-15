import React, { useState } from 'react';
import Header from './Header';
import './AIVoiceOrderPage.css';

const AIVoiceOrderPage = ({ onBack }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [finalTranscript, setFinalTranscript] = useState('');
  const [recognition, setRecognition] = useState(null);

  let transcriptBuffer = ''; // Local variable to accumulate the transcript

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
      transcriptBuffer = ''; // Clear the buffer when starting a new recording
    };

    recognitionInstance.onresult = (event) => {
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          transcriptBuffer += event.results[i][0].transcript;
        }
      }
    };

    recognitionInstance.onend = () => {
      setIsRecording(false);
      setFinalTranscript(transcriptBuffer); // Update state with the full transcript
      sendTranscriptToBackend(transcriptBuffer); // Send the transcript after stopping
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

  const sendTranscriptToBackend = (transcript) => {
    if (!transcript) {
      console.warn('Transcript is empty, nothing to send.');
      return;
    }

    fetch('http://localhost:3001/api/voice-order', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ transcript }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data);
        // You can handle further actions here based on the response from the backend
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <div>
      <Header showNavLinks={false} />
      <div className="ai-voice-order-container text-center">
        <h2>AI Voice Order</h2>
        <p>Press the button below to begin recording your order.</p>
        <div>
          <div className="transcript">
            <p>{finalTranscript}</p> {/* Show the final transcript */}
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
