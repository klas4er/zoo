import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UploadHistory from './pages/UploadHistory';
import LiveTranscription from './pages/LiveTranscription';
import AnimalProfile from './pages/AnimalProfile';
import Reports from './pages/Reports';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold text-gray-900">Zoo Keeper AI Assistant</h1>
          </div>
        </header>
        <main>
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/" element={<UploadHistory />} />
              <Route path="/live" element={<LiveTranscription />} />
              <Route path="/animal/:id" element={<AnimalProfile />} />
              <Route path="/reports" element={<Reports />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;