import { ColorScheme, ColorSchemeProvider, MantineProvider, Text } from '@mantine/core';
import { useState } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import ThemeButton from './components/navbar/theme_button';
import Dashboard from './pages/dashboard';


export default function App() {
  // const [colorScheme, setColorScheme] = useState<ColorScheme>('dark');
  // const toggleColorScheme = (value?: ColorScheme) =>
  //   setColorScheme(value || (colorScheme === 'dark' ? 'light' : 'dark'));
  
  return (
    <MantineProvider withGlobalStyles withNormalizeCSS>
      <MantineProvider theme={{ colorScheme: 'dark' }} withGlobalStyles withNormalizeCSS>
        <Text>Welcome to Mantine!</Text>
      </MantineProvider>

    </MantineProvider>
  );
}
