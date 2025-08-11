import { useState, useEffect } from 'react';
import axios from 'axios';

function HistoryPage() {
  const [target, setTarget] = useState('');
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    if (!target) return;
    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/api/history/${target}`);
      setHistory(res.data);
    } catch (err) {
      alert("Не удалось загрузить историю");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">История сканирований</h1>
      
      <div className="flex gap-2 mb-6">
        <input
          value={target}
          onChange={e => setTarget(e.target.value)}
          placeholder="Email, домен..."
          className="border p-2 flex-1"
        />
        <button onClick={fetchHistory} disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded">
          {loading ? "Загрузка..." : "Поиск"}
        </button>
      </div>

      {history && history.scans.length > 0 ? (
        <div>
          <h2 className="text-xl mb-3">Результаты для: <strong>{history.target}</strong></h2>
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-100">
                <th className="border px-4 py-2">Дата</th>
                <th className="border px-4 py-2">Модули</th>
                <th className="border px-4 py-2">Отчёт</th>
                <th className="border px-4 py-2">Риски</th>
              </tr>
            </thead>
            <tbody>
              {history.scans.map((scan, i) => (
                <tr key={i} className="hover:bg-gray-50">
                  <td className="border px-4 py-2">{new Date(scan.timestamp).toLocaleString()}</td>
                  <td className="border px-4 py-2">{scan.modules.join(", ")}</td>
                  <td className="border px-4 py-2">
                    {scan.report_pdf && <a href={scan.report_pdf} className="text-blue-600">PDF</a>}
                  </td>
                  <td className="border px-4 py-2">
                    <span className={`px-2 py-1 rounded text-xs ${scan.suspicious ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                      {scan.suspicious ? 'Высокий риск' : 'Норма'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : history && <p>Нет данных для этой цели.</p>}
    </div>
  );
}

export default HistoryPage;