import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { Box, Button, Group, Modal } from "@mantine/core";

export default function LoginButton() {
  const { loginWithRedirect, isAuthenticated, logout, user } = useAuth0();
  const [opened, setOpened] = React.useState(false);

  if (isAuthenticated) {
    return (
      <Box display={"inline-block"}>
        <button onClick={() => logout()}>Log Out</button>
        <Modal
        opened={opened}
        onClose={() => setOpened(false)}
        title="Your account"
        >
          <img src={user.picture} alt={user.name} />
          <h2>{user.name}</h2>
          <p>{user.email}</p>
        </Modal>

        <Group position="center">
          <Button onClick={() => setOpened(true)}>Open Modal</Button>
        </Group>
      </Box>
    
    );
  } else {
    return <button onClick={() => loginWithRedirect()}>Log In</button>;
  }

};
