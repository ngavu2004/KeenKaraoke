import React, { useState, useEffect, useRef } from 'react';
import lyricsData from '../../assets/response.json'; // Import the JSON file
import styles from './lyricsPage.module.css';
import backgroundImage from "../../image.png"; // Ensure this path is correct
import instrumental from '../../assets/instrumental.mp3'; // Import the audio file

const LyricsPage = () => {
  const [currentTime, setCurrentTime] = useState(0);
  const audioRef = useRef(null); // Reference for the audio element

  useEffect(() => {
    const audio = audioRef.current;

    // Set up a listener to update the current time based on the audio's progress
    const updateCurrentTime = () => {
      setCurrentTime(audio.currentTime);
    };

    // Add the timeupdate event listener to the audio element
    audio.addEventListener('timeupdate', updateCurrentTime);

    return () => {
      // Clean up the event listener when the component is unmounted
      audio.removeEventListener('timeupdate', updateCurrentTime);
    };
  }, []);

  const renderLyrics = () => {
    return lyricsData.segments.map((segment, index) => {
      const isCurrent = currentTime >= segment.start && currentTime < segment.end;

      return (
        <div
          key={index}
          style={{
            fontWeight: isCurrent ? 'bold' : 'normal',
            opacity: isCurrent ? 1 : 0.5,
            transition: 'opacity 0.5s ease-in-out',
            fontSize: isCurrent ? '30px' : '20px',
            color: 'white', // Ensure lyrics are visible
          }}
        >
          {segment.text}
        </div>
      );
    });
  };

  return (
    <div
      className={styles.container}
      style={{ backgroundImage: `url(${backgroundImage})` }} // Proper background image handling
    >
      <div className={styles.lyricsContainer}>
        <h2 className={styles.title}>Song Lyrics</h2>
        <div className={styles.lyrics}>{renderLyrics()}</div>

        {/* Audio player to play the instrumental file */}
        <audio ref={audioRef} controls>
          <source src={instrumental} type="audio/mp3" />
          Your browser does not support the audio element.
        </audio>
      </div>
    </div>
  );
};

export default LyricsPage;
