import { useContext } from 'react';
import AudioPlayerContext from '../context/AudioPlayerContext';

export const useAudioPlayer = () => {
  const context = useContext(AudioPlayerContext);
  if (!context) {
    throw new Error('useAudioPlayer debe ser usado dentro de un AudioPlayerProvider');
  }
  return context;
};
