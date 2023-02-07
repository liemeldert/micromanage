import React, { useEffect, useState } from "react";
import { Table } from "@mantine/core";
import { useAuth0 } from "@auth0/auth0-react";

export default function DataTable() {
  // Clean this up later
  const {
    // Auth state:
    error,
    isAuthenticated,
    isLoading,
    user,
    // Auth methods:
    getAccessTokenSilently,
    getAccessTokenWithPopup,
    getIdTokenClaims,
    loginWithRedirect,
    loginWithPopup,
    logout,
  } = useAuth0();
  

  useEffect(() => {

    const [rows, setRows] = useState()

    async function callApi() {
      try {
        const token = await getAccessTokenSilently();

        const response = await fetch(import.meta.env.VITE_API_URL, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        const responseData = await response.json();
        console.log(responseData);
        if (responseData === null) {
          console.log("No data");
          
        }
        const effect_rows = responseData.map((row) => (
          <tr key={row.name}>

        </tr>
        ));
      } catch (error) {
        console.error(error);
      }
    }

    callApi();
  }, []);
    
      return (
        <Table>
          <thead>
            <tr>
              <th>Device hostname</th>
              <th>Serial Number</th>
              <th>Symbol</th>
              <th>Atomic mass</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </Table>
      );    

}
