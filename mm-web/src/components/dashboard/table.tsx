import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";

interface TableRow {
  [key: string]: any;
}

interface AuthenticatedTableProps {
  url: string;
}

function AuthenticatedTable({ url }: AuthenticatedTableProps) {
  const [data, setData] = useState<TableRow[]>([]);
  const { getAccessTokenSilently } = useAuth0();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = await getAccessTokenSilently();
        const response = await fetch(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const json = await response.json();
        setData(json);
      } catch (error) {
        console.error(error);
      }
    };
    fetchData();
  }, [getAccessTokenSilently, url]);

  return (
    <table>
      <thead>
        <tr>
          {data.length > 0 &&
            Object.keys(data[0]).map((key) => <th key={key}>{key}</th>)}
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            {Object.values(row).map((value, index) => (
              <td key={index}>{value}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default AuthenticatedTable;
