import React, { useState } from 'react';

export const FileUpload = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('');

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/analyze-portfolio', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setStatus('✅ Analysis Triggered!');
        if (onUploadSuccess) onUploadSuccess();
      } else {
        setStatus('❌ Upload failed.');
      }
    } catch (err) {
      setStatus('❌ Server error.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl border-2 border-dashed border-slate-200 hover:border-blue-400 transition-colors mb-8 text-center">
      <input 
        type="file" 
        id="fileInput" 
        className="hidden" 
        onChange={handleFileChange}
        accept=".csv,.xlsx"
      />
      <label htmlFor="fileInput" className="cursor-pointer">
        <div className="text-3xl mb-2">📁</div>
        <p className="text-sm font-bold text-slate-700">Upload Broker Statement</p>
        <p className="text-xs text-slate-400 mt-1">Click to browse or drag & drop CSV</p>
      </label>
      
      {status && (
        <p className={`mt-3 text-[10px] font-black uppercase tracking-widest ${
          status.includes('✅') ? 'text-emerald-500' : 'text-slate-500'
        }`}>
          {status}
        </p>
      )}
    </div>
  );
};