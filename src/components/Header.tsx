import React from 'react';
import { Building2, Github, ExternalLink } from 'lucide-react';

export function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-effect">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-primary-500 to-accent-500 rounded-lg">
              <Building2 className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">FloorplanAI</h1>
              <p className="text-xs text-gray-600">Architectural Intelligence</p>
            </div>
          </div>
          
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-gray-700 hover:text-primary-600 transition-colors">
              Features
            </a>
            <a href="#how-it-works" className="text-gray-700 hover:text-primary-600 transition-colors">
              How it Works
            </a>
            <a href="#upload" className="btn-primary">
              Try Now
            </a>
          </nav>

          <div className="flex items-center space-x-4">
            <a 
              href="https://github.com/your-repo" 
              className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
              aria-label="GitHub Repository"
            >
              <Github className="h-5 w-5" />
            </a>
            <a 
              href="/docs" 
              className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
              aria-label="API Documentation"
            >
              <ExternalLink className="h-5 w-5" />
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}