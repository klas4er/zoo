import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, PieChart, Pie, Cell
} from 'recharts';

const AnimalProfile: React.FC = () => {
  const { id } = useParams();
  const [observations, setObservations] = useState<any[]>([]);
  
  // Mock data for charts
  const temperatureData = [
    { date: '2025-08-25', temperature: 37.2 },
    { date: '2025-08-26', temperature: 37.5 },
    { date: '2025-08-27', temperature: 37.8 },
    { date: '2025-08-28', temperature: 37.6 },
    { date: '2025-08-29', temperature: 37.9 },
    { date: '2025-08-30', temperature: 37.7 },
  ];
  
  const weightData = [
    { date: '2025-08-25', weight: 850 },
    { date: '2025-08-26', weight: 852 },
    { date: '2025-08-27', weight: 848 },
    { date: '2025-08-28', weight: 851 },
    { date: '2025-08-29', weight: 849 },
    { date: '2025-08-30', weight: 853 },
  ];
  
  const behaviorData = [
    { name: 'Calm', value: 45 },
    { name: 'Playful', value: 30 },
    { name: 'Aggressive', value: 15 },
    { name: 'Lethargic', value: 10 },
  ];
  
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="px-4 py-6 sm:px-0">
      <h2 className="text-2xl font-bold mb-4">Animal Profile</h2>
      
      {/* Animal Info */}
      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <div className="flex items-center">
          <div className="bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16 mr-4" />
          <div>
            <h3 className="text-xl font-semibold">Жужа (Giraffe)</h3>
            <p className="text-gray-600">ID: {id}</p>
            <p className="text-gray-600">Age: 8 years</p>
            <p className="text-gray-600">Enclosure: Zone C, Enclosure 12</p>
          </div>
        </div>
      </div>
      
      {/* Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        {/* Temperature Chart */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Temperature Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={temperatureData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis domain={[35, 40]} />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="temperature" 
                stroke="#8884d8" 
                activeDot={{ r: 8 }} 
                name="Temperature (°C)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        
        {/* Weight Chart */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Weight Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weightData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="weight" fill="#82ca9d" name="Weight (kg)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      
      {/* Behavior Distribution */}
      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <h3 className="text-lg font-semibold mb-4">Behavior Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={behaviorData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {behaviorData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      
      {/* Observations Feed */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-semibold mb-4">Observation Feed</h3>
        <div className="space-y-4">
          <div className="border border-gray-200 rounded p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="font-medium">Keeper: Ivan Petrov</span>
              <span className="text-gray-500 text-sm">2025-08-30 10:30</span>
            </div>
            <p className="mb-2">Самка жирафа Жужа ела 700 грамм люцерны, температура 37.8, спокойное поведение</p>
            <div className="flex flex-wrap gap-2">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                animal: giraffe (Жужа)
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                feeding: 700g alfalfa
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                vitals: 37.8°C
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                behavior: calm
              </span>
            </div>
          </div>
          
          <div className="border border-gray-200 rounded p-4">
            <div className="flex justify-between items-center mb-2">
              <span className="font-medium">Keeper: Maria Smirnova</span>
              <span className="text-gray-500 text-sm">2025-08-29 15:45</span>
            </div>
            <p className="mb-2">Жужа показывает игривое поведение, вес 850 кг, активно двигается по вольеру</p>
            <div className="flex flex-wrap gap-2">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                animal: giraffe (Жужа)
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                vitals: 850kg
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                behavior: playful
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                location: Zone C
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnimalProfile;