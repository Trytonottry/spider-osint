import { useState } from 'react';
import axios from 'axios';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import ScanPage from './pages/ScanPage';
import HistoryPage from './pages/HistoryPage';

const router = createBrowserRouter([
  { path: "/", element: <ScanPage /> },
  { path: "/history", element: <HistoryPage /> }
]);

function App() {
  return <RouterProvider router={router} />;
}

function App() {
  const [target, setTarget] = useState('');
  const [result, setResult] = useState(null);

  const scan = async () => {
    const res = await axios.post('http://localhost:8000/scan', { target });
    setResult("Сканирование запущено. Проверьте папку reports.");
  };

  return (
    <div className="p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">🕷️ SPIDER OSINT</h1>
      <input
        value={target}
        onChange={e => setTarget(e.target.value)}
        placeholder="Email, имя, домен..."
        className="border p-2 w-full mb-4"
      />
      <button onClick={scan} className="bg-red-600 text-white px-6 py-2 rounded">
        Сканировать
      </button>
      {result && <p className="mt-4 text-green-600">{result}</p>}
    </div>
  );
}

export default App;