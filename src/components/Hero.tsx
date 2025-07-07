import React from 'react';
import { ArrowRight, Zap, Shield, Target } from 'lucide-react';
import { motion } from 'framer-motion';

export function Hero() {
  const scrollToUpload = () => {
    document.getElementById('upload')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className="pt-24 pb-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              AI-Powered{' '}
              <span className="gradient-text">Floorplan</span>
              <br />
              Recognition System
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Automatically detect and analyze architectural elements in 2D floorplan sketches. 
              Our advanced Mask R-CNN model identifies walls, windows, and doors with precision.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="flex flex-col sm:flex-row gap-4 justify-center mb-12"
          >
            <button 
              onClick={scrollToUpload}
              className="btn-primary flex items-center justify-center space-x-2"
            >
              <span>Start Analysis</span>
              <ArrowRight className="h-5 w-5" />
            </button>
            <button className="btn-secondary">
              View Documentation
            </button>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto"
          >
            <div className="flex flex-col items-center p-6 glass-effect rounded-xl">
              <div className="p-3 bg-primary-100 rounded-lg mb-4">
                <Zap className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Lightning Fast</h3>
              <p className="text-gray-600 text-center">
                Process floorplans in seconds with our optimized AI pipeline
              </p>
            </div>

            <div className="flex flex-col items-center p-6 glass-effect rounded-xl">
              <div className="p-3 bg-accent-100 rounded-lg mb-4">
                <Target className="h-6 w-6 text-accent-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">High Accuracy</h3>
              <p className="text-gray-600 text-center">
                95%+ detection accuracy powered by advanced Mask R-CNN technology
              </p>
            </div>

            <div className="flex flex-col items-center p-6 glass-effect rounded-xl">
              <div className="p-3 bg-green-100 rounded-lg mb-4">
                <Shield className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure & Private</h3>
              <p className="text-gray-600 text-center">
                Your floorplans are processed securely and never stored permanently
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}