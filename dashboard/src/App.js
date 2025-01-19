import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import AnalyticsView from './components/AnalyticsView';
import FilterConfig from './components/FilterConfig';
import ChatInterface from './components/ChatInterface';
import NotFound from './components/NotFound';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Layout>
      <Routes>
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <AnalyticsView />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/filters" 
          element={
            <ProtectedRoute>
              <FilterConfig />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/chat" 
          element={
            <ProtectedRoute>
              <ChatInterface />
            </ProtectedRoute>
          } 
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Layout>
  );
}

export default App;
