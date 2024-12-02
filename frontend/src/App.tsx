import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import HomePage from './pages/main'

const App: React.FC = () => (
  <Router>
    <Routes>
      <Route path="/" element={<HomePage />} />
      
    </Routes>
  </Router>
);


export default App;
