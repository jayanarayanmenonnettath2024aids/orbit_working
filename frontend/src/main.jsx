import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/orbit-design-system.css';
import './App.css';
import './test-css-wiring.css'; /* TEMPORARY TEST - REMOVE AFTER VERIFICATION */

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
