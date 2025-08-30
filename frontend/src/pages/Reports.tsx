import React, { useState } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, PieChart, Pie, Cell
} from 'recharts';

const Reports: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string>('2025-08-30');
  
  // Mock data for charts
  const animalTemperatureData = [
    { animal: 'Жужа (Giraffe)', temperature: 37.7 },
    { animal: 'Dima (Elephant)', temperature: 36.5 },
    { animal: 'Sonya (Bear)', temperature: 38.2 },
    { animal: 'Rita (Lion)', temperature: 39.1 },
  ];
  
  const alertsData = [
    { animal: 'Rita (Lion)', severity: 'High', message: 'Aggressive behavior detected', count: 3 },
    { animal: 'Sonya (Bear)', severity: 'Medium', message: 'Slight weight loss', count: 1 },
    { animal: 'Unknown Tiger', severity: 'High', message: 'Abnormal temperature: 41.2°C', count: 1 },
  ];
  
  const behaviorDistributionData = [
    { name: 'Calm', value: 45 },
    { name: 'Playful', value: 30 },
    { name: 'Aggressive', value: 15 },
    { name: 'Lethargic', value: 10 },
  ];
  
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="px-4 py-6 sm:px-0">
      <h2 className="text-2xl font-bold mb-4">Daily Reports</h2>
      
      {/* Date Selector */}
      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <div className="flex items-center space-x-4">
          <label className="block text-gray-700 text-sm font-bold">
            Select Date:
          </label>
          <input 
            type="date" 
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="border border-gray-300 rounded px-3 py-2"
          />
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Generate Report
          </button>
          <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
            Export CSV
          </button>
          <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
            Export PDF
          </button>
        </div>
      </div>
      
      {/* Temperature Overview */}
      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <h3 className="text-lg font-semibold mb-4">Animal Temperature Overview</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={animalTemperatureData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="animal" />
            <YAxis domain={[35, 42]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="temperature" fill="#8884d8" name="Temperature (°C)" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      
      {/* Alerts Section */}
      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <h3 className="text-lg font-semibold mb-4">Alerts</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Animal</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Severity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Message</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Count</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {alertsData.map((alert, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap">{alert.animal}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      alert.severity === 'High' ? 'bg-red-100 text-red-800' : 
                      alert.severity === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 
                      'bg-green-100 text-green-800'
                    }`}>
                      {alert.severity}
                    </span>
                  </td>
                  <td className="px-6 py-4">{alert.message}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{alert.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      {/* Behavior Distribution */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Overall Behavior Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={behaviorDistributionData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {behaviorDistributionData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Reports;