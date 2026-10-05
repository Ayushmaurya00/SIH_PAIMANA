import React from 'react';
import { Upload, FileSpreadsheet, FileText, Trash2 } from 'lucide-react';

export const ImportDropzone = ({
  selectedFiles,
  isDragging,
  handleDragOver,
  handleDragLeave,
  handleDrop,
  fileInputRef,
  handleFileChange,
  removeFile,
  referenceMonth,
  setReferenceMonth
}) => {
  return (
    <div className="space-y-4">
      {/* Dropzone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
          isDragging
            ? 'border-blue-500 bg-blue-50'
            : 'border-slate-300 hover:border-slate-400 bg-slate-50'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.csv"
          onChange={handleFileChange}
          className="hidden"
        />
        <div className="flex flex-col items-center justify-center">
          <div className="w-12 h-12 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center mb-2">
            <Upload className="w-5 h-5" />
          </div>
          <p className="text-xs font-bold text-slate-800">
            Click to upload or drag and drop files
          </p>
          <p className="text-[11px] text-slate-500 mt-1">
            Supports official MoSPI Flash Report <strong className="text-slate-700">.PDF</strong> (Table 6) & Unified CUF <strong className="text-slate-700">.CSV</strong>
          </p>
        </div>
      </div>

      {/* Selected Files List */}
      {selectedFiles.length > 0 && (
        <div className="space-y-2">
          <div className="text-[11px] font-mono uppercase text-slate-500 font-bold">
            Queue ({selectedFiles.length} file{selectedFiles.length > 1 ? 's' : ''})
          </div>
          <div className="max-h-36 overflow-y-auto space-y-1.5 pr-1">
            {selectedFiles.map((file, idx) => {
              const isCsv = file.name.toLowerCase().endsWith('.csv');
              return (
                <div
                  key={idx}
                  className="flex items-center justify-between p-2 rounded-lg bg-white border border-slate-200 text-xs"
                >
                  <div className="flex items-center gap-2 truncate">
                    {isCsv ? (
                      <FileSpreadsheet className="w-4 h-4 text-emerald-600 shrink-0" />
                    ) : (
                      <FileText className="w-4 h-4 text-red-600 shrink-0" />
                    )}
                    <span className="truncate font-medium text-slate-800">{file.name}</span>
                    <span className="text-[10px] text-slate-400 shrink-0">
                      ({(file.size / 1024).toFixed(0)} KB)
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile(idx);
                    }}
                    className="text-slate-400 hover:text-red-600 p-1 rounded transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Target Reference Month Input */}
      <div>
        <label className="block text-xs font-semibold text-slate-700 mb-1">
          Effective Monitoring Snapshot Month
        </label>
        <input
          type="date"
          value={referenceMonth}
          onChange={(e) => setReferenceMonth(e.target.value)}
          className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg bg-white focus:outline-hidden focus:ring-1 focus:ring-blue-500 font-mono"
        />
      </div>
    </div>
  );
};

export default ImportDropzone;
