import React from "react"
import { Container, Text } from "@mantine/core"
import { Modal, Button, Group } from '@mantine/core';
import { useState } from "react";
 
const DevelopmentInfo = () => {
    const [opened, setOpened] = useState(false);

    if (import.meta.env.MODE === "development") {
        return (
            <>
            <Modal
              opened={opened}
              onClose={() => setOpened(false)}
              title="Debug info!"
            >
                <Group>
                    <Text>
                    Auth0 Information:
                        domain: { import.meta.env.VITE_AUTH0_DOMAIN }
                        domain: { import.meta.env.VITE_AUTH0_CLIENT_ID }
                    </Text>

                </Group>
            </Modal>
      
            <Group position="center">
              <Button onClick={() => setOpened(true)}>Open Modal</Button>
            </Group>
          </>
        );
    }
    else {
        return (null);
    }

}

export default DevelopmentInfo;
