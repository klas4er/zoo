import React, { useState } from 'react';

const UploadHistory: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/audio/process', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      setUploadResult(result);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      <h2 className="text-2xl font-bold mb-4">Upload Audio & History</h2>
      
      {/* Upload Section */}
      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Upload WAV File
          </label>
          <input 
            type="file" 
            accept=".wav" 
            onChange={handleFileChange}
            className="mb-4"
          />
          <button 
            onClick={handleUpload}
            disabled={!file || isUploading}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
          >
            {isUploading ? 'Processing...' : 'Upload & Process'}
          </button>
        </div>
        
        {uploadResult && (
          <div className="mt-6">
            <h3 className="text-xl font-semibold mb-2">Processing Result</h3>
            <div className="border border-gray-200 rounded p-4">
              <p><strong>ID:</strong> {uploadResult.id}</p>
              <p><strong>Status:</strong> {uploadResult.status}</p>
              <p><strong>Duration:</strong> {uploadResult.duration_sec.toFixed(2)} seconds</p>
              <p><strong>WER:</strong> {uploadResult.wer ? uploadResult.wer.toFixed(2) : 'N/A'}</p>
              <p><strong>Text:</strong> {uploadResult.text}</p>
              <div className="mt-4">
                <h4 className="font-semibold">Extracted Entities:</h4>
                <pre className="bg-gray-100 p-2 mt-2 rounded overflow-x-auto">
                  {JSON.stringify(uploadResult.entities, null, 2)}
                </pre>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* History Section */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-xl font-semibold mb-4">Transcription History</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Text</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Entities</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              <tr>
                <td className="px-6 py-4 whitespace-nowrap">obs_123</td>
                <td className="px-6 py-4 whitespace-nowrap">2025-08-30 10:30</td>
                <td className="px-6 py-4">Самка жирафа Жужа ела 700 грамм люцерны, температура 37.8, спокойное поведение</td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    animal
                  </span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 ml-2">
                    feeding
                  </span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 ml-2">
                    vitals
                  </span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800 ml-2">
                    behavior
                  </span>
                </td>
              </tr>
              {/* More rows would be added here in a real implementation */}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default UploadHistory;