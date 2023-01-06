import { ColorScheme, ColorSchemeProvider, Footer, MantineProvider, Text } from '@mantine/core';
import { useState } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import LoginButton from './components/login/login_button';
import ThemeButton from './components/navbar/theme_button';
import Dashboard from './pages/dashboard';
import DevelopmentInfo from "./components/development/development_info"


export default function App() {
  // const [colorScheme, setColorScheme] = useState<ColorScheme>('dark');
  // const toggleColorScheme = (value?: ColorScheme) =>
  //   setColorScheme(value || (colorScheme === 'dark' ? 'light' : 'dark'));
  const devmode = import.meta.env.MODE

  let modal_trigger = null

  if (devmode === "development") {
    modal_trigger = <DevelopmentInfo />
  }

  return (
    <MantineProvider theme={{ colorScheme: 'dark' }} withGlobalStyles withNormalizeCSS>
      <DevelopmentInfo />
    </MantineProvider>
  );
}
