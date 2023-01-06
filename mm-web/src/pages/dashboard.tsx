import { useAuth0 } from '@auth0/auth0-react';
import { AppShell, MantineProvider, Text } from '@mantine/core';
import { useState, useEffect } from 'react';
import { DoubleNavbar } from '../components/navbar/navbar';

export default function Dashboard() {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();
  const [userMetadata, setUserMetadata] = useState(null);


  useEffect(() => {
    const getUserMetadata = async () => {
      const auth0_domain = import.meta.env.VITE_AUTH0_DOMAIN;
      const app_domain = import.meta.env.VITE_APP_DOMAIN;
  
      try {
        const accessToken = await getAccessTokenSilently({
          audience: `https://${auth0_domain}/api/v2/`,
          scope: "read:current_user",
        });
  
        const userDetailsByIdUrl = `https://${app_domain}/api/v2/users/${user.sub}`;
  
        const metadataResponse = await fetch(userDetailsByIdUrl, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
  
        const { user_metadata } = await metadataResponse.json();
  
        setUserMetadata(user_metadata);
      } catch (e) {
        console.log(e.message);
      }
    };
  
    getUserMetadata();
  }, [getAccessTokenSilently, user?.sub]);

  return (
    <>

    <DoubleNavbar />

    <Text>Welcome to Mantine!!!!</Text>
  </>
  );
  }
  