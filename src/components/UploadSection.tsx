import React, { useState, useCallback } from 'react';
import { Upload, Image, AlertCircle, CheckCircle, Download, Eye } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useToast } from './ui/Toast';
import { ResultsModal } from './ResultsModal';

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

export function UploadSection() {
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [results, setResults] = useState<DetectionResult | null>(null);
  const [showResults, setShowResults] = useState(false);
  const { showToast } = useToast();

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    const imageFile = files.find(file => file.type.startsWith('image/'));
    
    if (imageFile) {
      setUploadedFile(imageFile);
      showToast('File uploaded successfully!', 'success');
    } else {
      showToast('Please upload a valid image file', 'error');
    }
  }, [showToast]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setUploadedFile(file);
      showToast('File uploaded successfully!', 'success');
    } else {
      showToast('Please upload a valid image file', 'error');
    }
  }, [showToast]);

  const processFloorplan = async () => {
    if (!uploadedFile) return;

    setIsProcessing(true);
    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      const response = await fetch('/api/floorplan/detect', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to process floorplan');
      }

      const result: DetectionResult = await response.json();
      setResults(result);
      setShowResults(true);
      showToast('Floorplan processed successfully!', 'success');
    } catch (error) {
      console.error('Error processing floorplan:', error);
      showToast('Failed to process floorplan. Please try again.', 'error');
    } finally {
      setIsProcessing(false);
    }
  };

  const resetUpload = () => {
    setUploadedFile(null);
    setResults(null);
    setShowResults(false);
  };

  return (
    <section id="upload" className="py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Upload Your Floorplan
          </h2>
          <p className="text-lg text-gray-600">
            Upload a 2D floorplan sketch and let our AI identify architectural elements
          </p>
        </div>

        <div className="space-y-8">
          {/* Upload Area */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={`
              relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300
              ${isDragging 
                ? 'border-primary-400 bg-primary-50' 
                : uploadedFile 
                  ? 'border-green-400 bg-green-50' 
                  : 'border-gray-300 bg-white hover:border-primary-300 hover:bg-primary-25'
              }
            `}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            
            <div className="space-y-4">
              {uploadedFile ? (
                <div className="flex flex-col items-center">
                  <CheckCircle className="h-12 w-12 text-green-500 mb-4" />
                  <p className="text-lg font-semibold text-green-700">
                    {uploadedFile.name}
                  </p>
                  <p className="text-sm text-gray-600">
                    File size: {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                  <Upload className="h-12 w-12 text-gray-400 mb-4" />
                  <p className="text-lg font-semibold text-gray-700">
                    Drop your floorplan here or click to browse
                  </p>
                  <p className="text-sm text-gray-500">
                    Supports JPG, PNG, and other image formats
                  </p>
                </div>
              )}
            </div>
          </motion.div>

          {/* Action Buttons */}
          <AnimatePresence>
            {uploadedFile && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="flex flex-col sm:flex-row gap-4 justify-center"
              >
                <button
                  onClick={processFloorplan}
                  disabled={isProcessing}
                  className="btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isProcessing ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      <span>Processing...</span>
                    </>
                  ) : (
                    <>
                      <Image className="h-5 w-5" />
                      <span>Analyze Floorplan</span>
                    </>
                  )}
                </button>
                
                <button
                  onClick={resetUpload}
                  className="btn-secondary"
                >
                  Upload Different File
                </button>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Results Preview */}
          <AnimatePresence>
            {results && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Detection Results
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">
                      {results.elements.walls.length}
                    </div>
                    <div className="text-sm text-blue-700">Walls Detected</div>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-2xl font-bold text-green-600">
                      {results.elements.windows.length}
                    </div>
                    <div className="text-sm text-green-700">Windows Detected</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-2xl font-bold text-purple-600">
                      {results.elements.doors.length}
                    </div>
                    <div className="text-sm text-purple-700">Doors Detected</div>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <button
                    onClick={() => setShowResults(true)}
                    className="btn-primary flex items-center justify-center space-x-2"
                  >
                    <Eye className="h-5 w-5" />
                    <span>View Detailed Results</span>
                  </button>
                  
                  <a
                    href={results.image_url}
                    download={`${results.filename}_detected.jpg`}
                    className="btn-secondary flex items-center justify-center space-x-2"
                  >
                    <Download className="h-5 w-5" />
                    <span>Download Result</span>
                  </a>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Results Modal */}
        {results && (
          <ResultsModal
            isOpen={showResults}
            onClose={() => setShowResults(false)}
            results={results}
          />
        )}
      </div>
    </section>
  );
}