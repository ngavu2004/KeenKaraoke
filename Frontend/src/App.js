
import './App.css';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LyricsPage from './pages/Lyrics/lyricsPage';
import HomePage from './pages/Homepage/homepage';
//import ParticlesComponent from './components/config/particles';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/lyrics/:song" element={<LyricsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
