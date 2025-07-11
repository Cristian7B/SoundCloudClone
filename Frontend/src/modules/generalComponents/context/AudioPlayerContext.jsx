// Contexto de audio player para integrar con la búsqueda
import React, { createContext, useState } from 'react';

const AudioPlayerContext = createContext();

export const AudioPlayerProvider = ({ children }) => {
  const [currentSong, setCurrentSong] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audio, setAudio] = useState(null);

  const playSong = (song) => {
    if (audio) {
      audio.pause();
    }

    const newAudio = new Audio(song.archivo_audio);
    setAudio(newAudio);
    setCurrentSong(song);
    setIsPlaying(true);

    newAudio.play().catch(error => {
      console.error('Error playing song:', error);
      setIsPlaying(false);
    });

    newAudio.addEventListener('ended', () => {
      setIsPlaying(false);
    });
  };

  const pauseSong = () => {
    if (audio) {
      audio.pause();
      setIsPlaying(false);
    }
  };

  const resumeSong = () => {
    if (audio) {
      audio.play().then(() => {
        setIsPlaying(true);
      }).catch(error => {
        console.error('Error resuming song:', error);
      });
    }
  };

  const stopSong = () => {
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
      setIsPlaying(false);
    }
  };

  const value = {
    currentSong,
    isPlaying,
    playSong,
    pauseSong,
    resumeSong,
    stopSong,
  };

  return (
    <AudioPlayerContext.Provider value={value}>
      {children}
    </AudioPlayerContext.Provider>
  );
};

export default AudioPlayerContext;
