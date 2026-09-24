import React, { useState, useRef, useEffect } from 'react';
import { Upload, X, AlertCircle } from 'lucide-react';
import { importReportFiles } from '../api/client';
import { ImportDropzone } from './import/ImportDropzone';
import { ImportPipelineProgress } from './import/ImportPipelineProgress';
import { ImportResultSummary } from './import/ImportResultSummary';

export const ImportModal = ({ isOpen, onClose, onImportSuccess }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [referenceMonth, setReferenceMonth] = useState('2026-08-01');
  const [isUploading, setIsUploading] = useState(false);
  const [progressPct, setProgressPct] = useState(0);
  const [currentStageIdx, setCurrentStageIdx] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);
  const progressTimerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (progressTimerRef.current) clearInterval(progressTimerRef.current);
    };
  }, []);

  if (!isOpen) return null;

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files || []);
    if (files.length > 0) addFiles(files);
  };

  const addFiles = (files) => {
    const validFiles = [];
    const errors = [];
    files.forEach((file) => {
      const ext = file.name.split('.').pop().toLowerCase();
      if (ext === 'csv' || ext === 'pdf') {
        if (!selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
          validFiles.push(file);
        }
      } else {
        errors.push(file.name);
      }
    });

    if (errors.length > 0) {
      setError(`Unsupported files skipped: ${errors.join(', ')}. Only .PDF and .CSV files are supported.`);
    } else {
      setError(null);
    }

    if (validFiles.length > 0) {
      setSelectedFiles(prev => [...prev, ...validFiles]);
      setResult(null);
    }
  };

  const removeFile = (idx) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== idx));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (selectedFiles.length === 0 || isUploading) return;

    setIsUploading(true);
    setProgressPct(5);
    setCurrentStageIdx(0);
    setError(null);

    let currentPct = 5;
    progressTimerRef.current = setInterval(() => {
      currentPct += Math.random() * 6 + 2;
      if (currentPct > 95) currentPct = 95;
      setProgressPct(Math.round(currentPct));
      if (currentPct < 25) setCurrentStageIdx(0);
      else if (currentPct < 50) setCurrentStageIdx(1);
      else if (currentPct < 75) setCurrentStageIdx(2);
      else if (currentPct < 90) setCurrentStageIdx(3);
      else setCurrentStageIdx(4);
    }, 450);

    try {
      const res = await importReportFiles(selectedFiles, referenceMonth);
      if (progressTimerRef.current) clearInterval(progressTimerRef.current);
      setProgressPct(100);
      setCurrentStageIdx(4);
      setTimeout(() => {
        setResult(res);
        setIsUploading(false);
        if (onImportSuccess) onImportSuccess(res);
      }, 500);
    } catch (err) {
      if (progressTimerRef.current) clearInterval(progressTimerRef.current);
      setIsUploading(false);
      const serverMsg = err.response?.data?.message || err.response?.data?.detail || err.response?.data?.error;
      setError(serverMsg || err.message || 'Failed to process file import.');
    }
  };

  const handleReset = () => {
    setSelectedFiles([]);
    setResult(null);
    setError(null);
    setProgressPct(0);
    setCurrentStageIdx(0);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-950/50 backdrop-blur-xs flex items-center justify-center p-4 animate-fade-in">
      <div className="w-full max-w-xl bg-white rounded-xl border border-slate-200 shadow-2xl overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div className="p-5 border-b border-slate-200 flex items-center justify-between bg-white">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-[#0F2B5B] text-white flex items-center justify-center shrink-0 shadow-xs">
              <Upload className="w-4 h-4 text-white" aria-hidden="true" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                Import Flash Reports / Telemetry
                <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-100 text-slate-700 border border-slate-200 font-bold">
                  Batch Ingestion
                </span>
              </h3>
            </div>
          </div>
          {!isUploading && (
            <button onClick={onClose} aria-label="Close import modal" className="p-1 rounded-lg text-slate-500 hover:text-slate-700 hover:bg-slate-100">
              <X className="w-5 h-5" aria-hidden="true" />
            </button>
          )}
        </div>

        <div className="p-6">
          {error && (
            <div className="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 text-red-500" aria-hidden="true" />
              <span>{error}</span>
            </div>
          )}

          {isUploading ? (
            <ImportPipelineProgress progressPct={progressPct} currentStageIdx={currentStageIdx} />
          ) : result ? (
            <ImportResultSummary result={result} onClose={onClose} handleReset={handleReset} />
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5">
              <ImportDropzone
                selectedFiles={selectedFiles} isDragging={isDragging}
                handleDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                handleDragLeave={() => setIsDragging(false)}
                handleDrop={(e) => { e.preventDefault(); setIsDragging(false); addFiles(Array.from(e.dataTransfer.files || [])); }}
                fileInputRef={fileInputRef} handleFileChange={handleFileChange}
                removeFile={removeFile} referenceMonth={referenceMonth} setReferenceMonth={setReferenceMonth}
              />
              <div className="flex items-center justify-end gap-2 pt-3 border-t border-slate-200">
                <button type="button" onClick={onClose} className="text-xs px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 text-slate-700">Cancel</button>
                <button type="submit" disabled={selectedFiles.length === 0} className="btn-primary text-xs flex items-center gap-1.5 py-2 px-4 bg-blue-700 text-white rounded-lg disabled:opacity-50">
                  <Upload className="w-3.5 h-3.5" aria-hidden="true" />
                  <span>Start Pipeline Ingestion</span>
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImportModal;
