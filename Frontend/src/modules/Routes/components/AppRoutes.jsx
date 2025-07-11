import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Home } from '../../home/components/Home';
import { Library } from '../../library/components/Library';
import { PlaylistView } from '../../generalComponents/components/PlaylistView';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/home" replace />} />
      
      <Route path="/home" element={<Home />} />
      <Route path="/library" element={<Library />} />
      <Route path="/playlist/:playlistId" element={<PlaylistView />} />
      
      <Route path="*" element={<Navigate to="/home" replace />} />
    </Routes>
  );
};

export default AppRoutes;
