import React from 'react';
import { Brain, Layers, Zap, Shield, Download, BarChart3 } from 'lucide-react';
import { motion } from 'framer-motion';

const features = [
  {
    icon: Brain,
    title: 'Advanced AI Detection',
    description: 'Powered by Mask R-CNN deep learning model trained specifically for architectural element recognition.',
    color: 'from-blue-500 to-blue-600'
  },
  {
    icon: Layers,
    title: 'Multi-Element Recognition',
    description: 'Simultaneously detects walls, windows, and doors with precise boundary segmentation.',
    color: 'from-green-500 to-green-600'
  },
  {
    icon: Zap,
    title: 'Real-time Processing',
    description: 'Fast inference pipeline optimized for quick results without compromising accuracy.',
    color: 'from-yellow-500 to-yellow-600'
  },
  {
    icon: Shield,
    title: 'Secure & Private',
    description: 'Your floorplans are processed securely with no permanent storage of sensitive data.',
    color: 'from-purple-500 to-purple-600'
  },
  {
    icon: Download,
    title: 'Export Results',
    description: 'Download processed images and detailed JSON data for integration with your workflow.',
    color: 'from-indigo-500 to-indigo-600'
  },
  {
    icon: BarChart3,
    title: 'Confidence Scoring',
    description: 'Each detection includes confidence scores to help you assess the reliability of results.',
    color: 'from-red-500 to-red-600'
  }
];

export function Features() {
  return (
    <section id="features" className="py-16 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for
              <span className="gradient-text"> Architectural Analysis</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our AI-powered system combines cutting-edge technology with practical functionality 
              to deliver accurate and reliable floorplan analysis.
            </p>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="group p-6 bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-200 hover:shadow-xl transition-all duration-300"
            >
              <div className={`inline-flex p-3 rounded-lg bg-gradient-to-r ${feature.color} mb-4 group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="h-6 w-6 text-white" />
              </div>
              
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                {feature.title}
              </h3>
              
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="mt-16 text-center"
        >
          <div className="inline-flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-primary-50 to-accent-50 rounded-full border border-primary-200">
            <Brain className="h-5 w-5 text-primary-600" />
            <span className="text-primary-700 font-medium">
              Powered by state-of-the-art Mask R-CNN architecture
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}