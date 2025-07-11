import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../user';
import { NavigationProvider } from '../context/NavigationContext';
import Layout from './Layout';

const AppRouter = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <NavigationProvider>
          <Layout />
        </NavigationProvider>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default AppRouter;
