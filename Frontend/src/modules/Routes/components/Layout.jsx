import React from 'react';
import { Nav } from '../../generalComponents/components/Nav';
import AppRoutes from './AppRoutes';
import { ArtistTools } from '../../generalComponents/components/ArtistTools';

const Layout = () => {
  return (
    <>
      <div className="navContainer">
        <Nav />
      </div>
      <main className="generalContent">
        <AppRoutes />
        <ArtistTools />
      </main>
    </>
  );
};

export default Layout;
