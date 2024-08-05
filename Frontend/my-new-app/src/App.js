import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
// import axios from 'axios';
import './App.css';
import Home from './pages/Home.jsx';
import Player from './pages/PlayerPage.jsx';

function App () {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/player" element={<Player />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
