import React, { useState, useRef } from 'react';

const LiveTranscription: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [partialText, setPartialText] = useState('');
  const [finalText, setFinalText] = useState('');
  const [entities, setEntities] = useState<any>({});
  const [stats, setStats] = useState<any>({});
  const [error, setError] = useState<string | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);

  const startRecording = async () => {
    try {
      setIsRecording(true);
      setPartialText('');
      setFinalText('');
      setEntities({});
      setError(null);
      
      // Connect to WebSocket
      const wsUrl = `ws://localhost:8000/ws/transcribe?lang=ru&session_id=${Date.now()}`;
      wsRef.current = new WebSocket(wsUrl);
      
      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        switch (data.event) {
          case 'partial':
            setPartialText(data.text);
            break;
          case 'final':
            setFinalText(prev => prev + ' ' + data.text);
            break;
          case 'entity_update':
            setEntities(data.entities);
            break;
          case 'stats':
            setStats(data.stats);
            break;
          case 'error':
            setError(data.message);
            break;
        }
      };
      
      wsRef.current.onerror = (event) => {
        setError('WebSocket connection error');
        setIsRecording(false);
      };
      
      // Get microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Create audio context and processor
      audioContextRef.current = new AudioContext();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      const processor = audioContextRef.current.createScriptProcessor(4096, 1, 1);
      
      // Process audio chunks
      processor.onaudioprocess = (event) => {
        if (!isRecording || !wsRef.current) return;
        
        const inputData = event.inputBuffer.getChannelData(0);
        const pcmData = new Int16Array(inputData.length);
        
        // Convert float samples to 16-bit integers
        for (let i = 0; i < inputData.length; i++) {
          pcmData[i] = Math.max(-1, Math.min(1, inputData[i])) * 0x7FFF;
        }
        
        // Send PCM data to WebSocket if connected
        if (wsRef.current.readyState === WebSocket.OPEN) {
          wsRef.current.send(pcmData.buffer);
        }
      };
      
      source.connect(processor);
      processor.connect(audioContextRef.current.destination);
      
      // Store reference to media recorder (for potential future use)
      mediaRecorderRef.current = new MediaRecorder(stream);
      
    } catch (err) {
      setError('Failed to access microphone');
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    
    if (wsRef.current) {
      wsRef.current.close();
    }
    
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      <h2 className="text-2xl font-bold mb-4">Live Transcription</h2>
      
      {/* Recording Controls */}
      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <div className="flex space-x-4 mb-4">
          {!isRecording ? (
            <button 
              onClick={startRecording}
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            >
              Start Recording
            </button>
          ) : (
            <button 
              onClick={stopRecording}
              className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
            >
              Stop Recording
            </button>
          )}
        </div>
        
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
            Error: {error}
          </div>
        )}
        
        {/* Audio Level Indicator */}
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Audio Level
          </label>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div 
              className="bg-blue-600 h-2.5 rounded-full" 
              style={{ width: '45%' }} // This would be dynamically updated in a real implementation
            ></div>
          </div>
        </div>
        
        {/* Transcription Display */}
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Partial Transcription
          </label>
          <div className="border border-gray-300 rounded p-4 min-h-[100px] bg-gray-50">
            {partialText || 'Waiting for speech...'}
          </div>
        </div>
        
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Final Transcription
          </label>
          <div className="border border-gray-300 rounded p-4 min-h-[150px] bg-gray-50">
            {finalText}
          </div>
        </div>
        
        {/* Entities Display */}
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Extracted Entities
          </label>
          <div className="border border-gray-300 rounded p-4 bg-gray-50">
            {Object.keys(entities).length > 0 ? (
              <pre className="overflow-x-auto">
                {JSON.stringify(entities, null, 2)}
              </pre>
            ) : (
              'No entities extracted yet'
            )}
          </div>
        </div>
        
        {/* Stats Display */}
        <div>
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Performance Stats
          </label>
          <div className="border border-gray-300 rounded p-4 bg-gray-50">
            {Object.keys(stats).length > 0 ? (
              <div>
                <p>RTF: {stats.rtf}</p>
                <p>CPU Load: {stats.cpu_load}</p>
              </div>
            ) : (
              'No stats available'
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LiveTranscription;