import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [logs, setLogs] = useState([]);
  const [query, setQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [form, setForm] = useState({ timestamp: '', log_level: 'INFO', message: '', status: 'SUCCESS', compliance_status: 'COMPLIANT' });

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      const res = await axios.get('http://localhost:8000/logs/');
      setLogs(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/logs/', form);
      fetchLogs();
      setForm({ timestamp: '', log_level: 'INFO', message: '', status: 'SUCCESS', compliance_status: 'COMPLIANT' });
    } catch (err) {
      console.error(err);
    }
  };

  const handleAiQuery = async () => {
    try {
      const res = await axios.post('http://localhost:8000/query/', { query });
      setAiResponse(res.data.response || res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const totalLogs = logs.length;
  const compliantCount = logs.filter(l => l.compliance_status === 'COMPLIANT').length;
  const violationCount = totalLogs - compliantCount;

  return (
    <div style={{ fontFamily: 'Inter, sans-serif', backgroundColor: '#0f172a', color: '#f8fafc', minHeight: '100vh', padding: '30px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        
        {/* Header */}
        <header style={{ marginBottom: '30px', borderBottom: '1px solid #334155', paddingBottom: '20px' }}>
          <h1 style={{ margin: '0 0 5px 0', fontSize: '28px', color: '#38bdf8' }}>🛡️ AegisOps</h1>
          <p style={{ margin: 0, color: '#94a3b8' }}>Medical Compliance & Audit Intelligence Platform</p>
        </header>

        {/* Metrics Overview Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px', marginBottom: '30px' }}>
          <div style={{ background: '#1e293b', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #38bdf8' }}>
            <h4 style={{ margin: '0 0 10px 0', color: '#94a3b8' }}>Total Audit Logs</h4>
            <span style={{ fontSize: '24px', fontWeight: 'bold' }}>{totalLogs}</span>
          </div>
          <div style={{ background: '#1e293b', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #22c55e' }}>
            <h4 style={{ margin: '0 0 10px 0', color: '#94a3b8' }}>Compliant Records</h4>
            <span style={{ fontSize: '24px', fontWeight: 'bold', color: '#22c55e' }}>{compliantCount}</span>
          </div>
          <div style={{ background: '#1e293b', padding: '20px', borderRadius: '10px', borderLeft: '4px solid #ef4444' }}>
            <h4 style={{ margin: '0 0 10px 0', color: '#94a3b8' }}>Flagged Violations</h4>
            <span style={{ fontSize: '24px', fontWeight: 'bold', color: '#ef4444' }}>{violationCount}</span>
          </div>
        </div>

        {/* Main Grid: AI Query & Add Log Form */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px', marginBottom: '40px' }}>
          
          {/* AI Query Box */}
          <div style={{ background: '#1e293b', padding: '25px', borderRadius: '12px', border: '1px solid #334155' }}>
            <h3 style={{ marginTop: 0, color: '#38bdf8' }}>🤖 AI Compliance Query (RAG)</h3>
            <textarea 
              rows="3"
              value={query} 
              onChange={(e) => setQuery(e.target.value)} 
              placeholder="Ask about medical compliance or SOPs..." 
              style={{ width: '100%', padding: '12px', borderRadius: '8px', background: '#0f172a', color: '#fff', border: '1px solid #475569', marginBottom: '15px', resize: 'vertical' }}
            />
            <button onClick={handleAiQuery} style={{ background: '#0284c7', color: '#fff', border: 'none', padding: '10px 20px', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>Ask AI</button>
            {aiResponse && (
              <div style={{ marginTop: '15px', padding: '15px', background: '#0f172a', borderRadius: '8px', borderLeft: '4px solid #38bdf8', fontSize: '14px', lineHeight: '1.5' }}>
                <strong>Response:</strong> {aiResponse}
              </div>
            )}
          </div>

          {/* Add Log Form */}
          <div style={{ background: '#1e293b', padding: '25px', borderRadius: '12px', border: '1px solid #334155' }}>
            <h3 style={{ marginTop: 0, color: '#38bdf8' }}>📝 Record Compliance Event</h3>
            <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <input type="text" placeholder="Timestamp (ISO)" value={form.timestamp} onChange={(e) => setForm({...form, timestamp: e.target.value})} style={{ padding: '10px', borderRadius: '6px', background: '#0f172a', color: '#fff', border: '1px solid #475569' }} />
              <select value={form.log_level} onChange={(e) => setForm({...form, log_level: e.target.value})} style={{ padding: '10px', borderRadius: '6px', background: '#0f172a', color: '#fff', border: '1px solid #475569' }}>
                <option value="INFO">INFO</option>
                <option value="WARNING">WARNING</option>
                <option value="ERROR">ERROR</option>
              </select>
              <input type="text" placeholder="Compliance message..." value={form.message} onChange={(e) => setForm({...form, message: e.target.value})} style={{ gridColumn: 'span 2', padding: '10px', borderRadius: '6px', background: '#0f172a', color: '#fff', border: '1px solid #475569' }} />
              <select value={form.status} onChange={(e) => setForm({...form, status: e.target.value})} style={{ padding: '10px', borderRadius: '6px', background: '#0f172a', color: '#fff', border: '1px solid #475569' }}>
                <option value="SUCCESS">SUCCESS</option>
                <option value="FAILED">FAILED</option>
              </select>
              <select value={form.compliance_status} onChange={(e) => setForm({...form, compliance_status: e.target.value})} style={{ padding: '10px', borderRadius: '6px', background: '#0f172a', color: '#fff', border: '1px solid #475569' }}>
                <option value="COMPLIANT">COMPLIANT</option>
                <option value="VIOLATION">VIOLATION</option>
              </select>
              <button type="submit" style={{ gridColumn: 'span 2', padding: '12px', background: '#16a34a', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold' }}>Submit Log Entry</button>
            </form>
          </div>

        </div>

        {/* Logs Table */}
        <div style={{ background: '#1e293b', padding: '25px', borderRadius: '12px', border: '1px solid #334155' }}>
          <h3 style={{ marginTop: 0, marginBottom: '20px', color: '#38bdf8' }}>📊 System & Compliance Records</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #334155', color: '#94a3b8' }}>
                  <th style={{ padding: '12px' }}>ID</th>
                  <th style={{ padding: '12px' }}>Timestamp</th>
                  <th style={{ padding: '12px' }}>Level</th>
                  <th style={{ padding: '12px' }}>Message</th>
                  <th style={{ padding: '12px' }}>Status</th>
                  <th style={{ padding: '12px' }}>Compliance</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id} style={{ borderBottom: '1px solid #334155' }}>
                    <td style={{ padding: '12px', color: '#94a3b8' }}>#{log.id}</td>
                    <td style={{ padding: '12px' }}>{log.timestamp}</td>
                    <td style={{ padding: '12px' }}>
                      <span style={{ padding: '3px 8px', borderRadius: '4px', fontSize: '12px', background: log.log_level === 'ERROR' ? '#7f1d1d' : '#14532d', color: '#fff' }}>
                        {log.log_level}
                      </span>
                    </td>
                    <td style={{ padding: '12px' }}>{log.message}</td>
                    <td style={{ padding: '12px' }}>{log.status}</td>
                    <td style={{ padding: '12px' }}>
                      <span style={{ padding: '4px 10px', borderRadius: '20px', fontSize: '12px', fontWeight: 'bold', background: log.compliance_status === 'COMPLIANT' ? '#065f46' : '#991b1b', color: log.compliance_status === 'COMPLIANT' ? '#34d399' : '#fca5a5' }}>
                        {log.compliance_status || 'COMPLIANT'}
                      </span>
                    </td>
                  </tr>
                ))}
                {logs.length === 0 && (
                  <tr>
                    <td colSpan="6" style={{ padding: '20px', textAlign: 'center', color: '#94a3b8' }}>No records found in database.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;