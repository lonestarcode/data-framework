import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SummaryList } from './components/SummaryList';
import { SourceManager } from './components/SourceManager';
import { SearchBar } from './components/SearchBar';
import { Navigation } from './components/Navigation';
import { ProtectedRoute } from './components/ProtectedRoute';

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <SearchBar />
      <Routes>
        <Route path="/" element={<SummaryList />} />
        <Route 
          path="/sources" 
          element={
            <ProtectedRoute element={<SourceManager />} />
          } 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App; 