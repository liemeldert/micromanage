import React from 'react'
import { MantineProvider, ColorSchemeProvider, ColorScheme, Navbar, MantineThemeOverride } from '@mantine/core';
import ReactDOM from 'react-dom/client'
import App from './App'
import {
  createBrowserRouter,
  RouterProvider,
  Route,
} from "react-router-dom";
import { useState } from 'react';
import Index from './pages';
import { DoubleNavbar } from './components/navbar/navbar';
import Dashboard from './pages/dashboard';
import { Auth0Provider } from "@auth0/auth0-react";
import { meta } from '@mantine/ds';
import Landing from './pages/landing';


export const globalTheme: MantineThemeOverride = {
  // Font sizes in px, other units are not supported
  fontSizes: {
    xs: 10,
    sm: 12,
    md: 16,
    lg: 28,
    xl: 32,
  },
  colorScheme: 'dark',
}


const router = createBrowserRouter([
  {
    path: "/application/",
    element: <App />,
    children: [
      {
        path: "/application/dashboard",
        element: <Dashboard />,
      },
    ],
  },
  {
    path: "/",
    element: <Landing />,
  }
]);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <Auth0Provider
    domain={import.meta.env.VITE_AUTH0_DOMAIN}
    clientId={import.meta.env.VITE_AUTH0_CLEINT_ID}
    redirectUri={window.location.origin}
  >
      <RouterProvider router={router} />
  </Auth0Provider>
  </React.StrictMode>
)
