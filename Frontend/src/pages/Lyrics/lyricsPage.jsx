import React, { useState, useEffect } from 'react';
import lyricsData from '../../song.json'; // Import the JSON file
import styles from './lyricsPage.module.css';

const LyricsPage = () => {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    // Simulate song progress (replace with actual song's time later)
    const interval = setInterval(() => {
      setCurrentTime(prevTime => prevTime + 1);
    }, 1000); // Update time every second

    return () => clearInterval(interval);
  }, []);

  const renderLyrics = () => {
    return lyricsData.lyrics.map((lyric, index) => {
      const isCurrent = currentTime >= lyric.timestamp &&
        (index === lyricsData.lyrics.length - 1 || currentTime < lyricsData.lyrics[index + 1].timestamp);
      return (
        <div
          key={lyric.timestamp}
          style={{
            fontWeight: isCurrent ? 'bold' : 'normal',
            opacity: isCurrent ? 1 : 0.5,
            transition: 'opacity 0.5s ease-in-out',
            fontSize: isCurrent ? '30px' : '20px',
            color: 'white', // Ensure lyrics are visible over background
          }}
        >
          {lyric.line}
        </div>
      );
    });
  };

  return (
    <div className={styles.container} style={{ backgroundImage: `url(${lyricsData.image})` }}>
      <h2 className={styles.title}>Song Lyrics</h2>
      <div className={styles.lyrics}>{renderLyrics()}</div>
    </div>
  );
};

export default LyricsPage;
