import React from 'react';
import { X, Download, Copy, CheckCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useToast } from './ui/Toast';

interface DetectionResult {
  id: string;
  filename: string;
  elements: {
    walls: Array<{
      type: string;
      confidence: number;
      bbox: number[];
      contour: number[][];
    }>;
    windows: Array<{
      type: string;
      confidence: number;
      bbox: number[];
      contour: number[][];
    }>;
    doors: Array<{
      type: string;
      confidence: number;
      bbox: number[];
      contour: number[][];
    }>;
  };
  image_url: string;
}

interface ResultsModalProps {
  isOpen: boolean;
  onClose: () => void;
  results: DetectionResult;
}

export function ResultsModal({ isOpen, onClose, results }: ResultsModalProps) {
  const { showToast } = useToast();

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      showToast('Copied to clipboard!', 'success');
    } catch (error) {
      showToast('Failed to copy to clipboard', 'error');
    }
  };

  const exportResults = () => {
    const dataStr = JSON.stringify(results, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${results.filename}_results.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const allElements = [
    ...results.elements.walls.map(w => ({ ...w, category: 'Wall', color: 'blue' })),
    ...results.elements.windows.map(w => ({ ...w, category: 'Window', color: 'green' })),
    ...results.elements.doors.map(d => ({ ...d, category: 'Door', color: 'purple' }))
  ].sort((a, b) => b.confidence - a.confidence);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm"
            onClick={onClose}
          />
          
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="relative bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <div>
                <h2 className="text-2xl font-bold text-gray-900">Detection Results</h2>
                <p className="text-sm text-gray-600">{results.filename}</p>
              </div>
              <button
                onClick={onClose}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="h-6 w-6" />
              </button>
            </div>

            <div className="overflow-y-auto max-h-[calc(90vh-120px)]">
              {/* Summary Stats */}
              <div className="p-6 border-b border-gray-200">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-3xl font-bold text-blue-600">
                      {results.elements.walls.length}
                    </div>
                    <div className="text-sm text-blue-700 font-medium">Walls</div>
                    <div className="text-xs text-blue-600">
                      Avg: {results.elements.walls.length > 0 
                        ? (results.elements.walls.reduce((sum, w) => sum + w.confidence, 0) / results.elements.walls.length * 100).toFixed(1)
                        : 0}% confidence
                    </div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-3xl font-bold text-green-600">
                      {results.elements.windows.length}
                    </div>
                    <div className="text-sm text-green-700 font-medium">Windows</div>
                    <div className="text-xs text-green-600">
                      Avg: {results.elements.windows.length > 0 
                        ? (results.elements.windows.reduce((sum, w) => sum + w.confidence, 0) / results.elements.windows.length * 100).toFixed(1)
                        : 0}% confidence
                    </div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-3xl font-bold text-purple-600">
                      {results.elements.doors.length}
                    </div>
                    <div className="text-sm text-purple-700 font-medium">Doors</div>
                    <div className="text-xs text-purple-600">
                      Avg: {results.elements.doors.length > 0 
                        ? (results.elements.doors.reduce((sum, d) => sum + d.confidence, 0) / results.elements.doors.length * 100).toFixed(1)
                        : 0}% confidence
                    </div>
                  </div>
                </div>
              </div>

              {/* Detected Image */}
              <div className="p-6 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Processed Image</h3>
                <div className="relative bg-gray-100 rounded-lg overflow-hidden">
                  <img
                    src={results.image_url}
                    alt="Detected floorplan"
                    className="w-full h-auto max-h-96 object-contain"
                  />
                </div>
              </div>

              {/* Detailed Results */}
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Detected Elements ({allElements.length})
                  </h3>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => copyToClipboard(JSON.stringify(results, null, 2))}
                      className="flex items-center space-x-2 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                    >
                      <Copy className="h-4 w-4" />
                      <span>Copy JSON</span>
                    </button>
                    <button
                      onClick={exportResults}
                      className="flex items-center space-x-2 px-3 py-2 text-sm bg-primary-100 hover:bg-primary-200 text-primary-700 rounded-lg transition-colors"
                    >
                      <Download className="h-4 w-4" />
                      <span>Export</span>
                    </button>
                  </div>
                </div>

                <div className="space-y-3 max-h-64 overflow-y-auto">
                  {allElements.map((element, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border-l-4 ${
                        element.color === 'blue' 
                          ? 'bg-blue-50 border-blue-400' 
                          : element.color === 'green'
                          ? 'bg-green-50 border-green-400'
                          : 'bg-purple-50 border-purple-400'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div className={`w-3 h-3 rounded-full ${
                            element.color === 'blue' 
                              ? 'bg-blue-500' 
                              : element.color === 'green'
                              ? 'bg-green-500'
                              : 'bg-purple-500'
                          }`} />
                          <span className="font-medium text-gray-900">
                            {element.category}
                          </span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <CheckCircle className="h-4 w-4 text-green-500" />
                          <span className="text-sm font-medium text-gray-700">
                            {(element.confidence * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                      <div className="mt-2 text-xs text-gray-600">
                        Bounding Box: [{element.bbox.map(b => b.toFixed(0)).join(', ')}]
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}