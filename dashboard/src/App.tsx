import React from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import store from './store/store';

// Components
import { Layout } from './components/Layout';
import { AnalyticsView } from './components/AnalyticsView';
import { FilterConfig } from './components/FilterConfig';
import { ChatInterface } from './components/ChatInterface';
import { NotFound } from './components/NotFound';
import { ProtectedRoute } from './components/ProtectedRoute';

// Styles
import './index.css';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={
              <ProtectedRoute>
                <AnalyticsView />
              </ProtectedRoute>
            } />
            
            <Route path="/filters" element={
              <ProtectedRoute>
                <FilterConfig />
              </ProtectedRoute>
            } />
            
            <Route path="/chat" element={
              <ProtectedRoute>
                <ChatInterface />
              </ProtectedRoute>
            } />
            
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
      </Router>
    </Provider>
  );
};

export default App;
