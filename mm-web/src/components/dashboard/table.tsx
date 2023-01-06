import React, { useEffect } from "react";
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
    async function callApi() {
      try {
        const token = await getTokenSilently();

        const response = await fetch("https://my-api.com/endpoint", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        const responseData = await response.json();
        console.log(responseData);
      } catch (error) {
        console.error(error);
      }
    }

    callApi();
  }, []);



    const rows = elements.map((element) => (
        <tr key={element.name}>
          <td>{element.position}</td>
          <td>{element.name}</td>
          <td>{element.symbol}</td>
          <td>{element.mass}</td>
        </tr>
      ));
    
      return (
        <Table>
          <thead>
            <tr>
              <th>Element position</th>
              <th>Element name</th>
              <th>Symbol</th>
              <th>Atomic mass</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </Table>
      );    

}
