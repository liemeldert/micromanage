import React, { useCallback } from "react";
import { Box, MantineProvider, Text, Grid, ScrollArea, Center } from "@mantine/core";
import { globalTheme } from "../main";
import { useViewportSize } from "@mantine/hooks";
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles"
import type { Container, Engine } from "tsparticles-engine";
import FlowingGradientBackground from "../components/gradient";
import LoginButton from "../components/login/login_button";

const Landing = () => {

    const {height, width} = useViewportSize();

    const [gradient_angle, set_gradient_angle] = React.useState(45);

    React.useEffect(() => {
        const interval = setInterval(() => {
            set_gradient_angle(gradient_angle + 1);
        }, 500);
        return () => clearInterval(interval);
    }, [gradient_angle]);
    
    const particlesInit = useCallback(async (engine: Engine) => {
        console.log(engine);

        // you can initialize the tsParticles instance (engine) here, adding custom shapes or presets
        // this loads the tsparticles package bundle, it's the easiest method for getting everything ready
        // starting from v2 you can add only the features you need reducing the bundle size
        await loadFull(engine);
    }, []);

    const particlesLoaded = useCallback(async (container: Container | undefined) => {
        await console.log(container);
    }, []);

    return (
        <MantineProvider theme={ globalTheme } withGlobalStyles withNormalizeCSS>

            <Box
                sx={(theme) => ({
                    background: theme.fn.linearGradient(gradient_angle, 'red', 'blue'),
                })}
                h={ height }
            >

                <Grid grow gutter="xs" p="lg" >
                    <Grid.Col span={1} sx={(theme) => ({
                    zIndex: 10,
                })}>
                        <Box
                            sx={(theme) => ({
                                backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[5] : theme.colors.gray[1],
                                height: height - theme.spacing.xl * 2,
                                padding: theme.spacing.xl,
                                borderRadius: theme.radius.md,
                                opacity: 0.9,
                        })}>
                            <Text
                                variant="gradient"
                                gradient={{ from: 'indigo', to: 'cyan', deg: 45 }}
                                sx={{ fontFamily: 'Greycliff CF, sans-serif' }}
                                fz="xl"
                                fw={700}
                                >
                                Micromanage.
                            </Text>
                            <Text>      Simple application management.</Text>

                            <Center>
                                <LoginButton />
                            </Center>
                            
                        </Box>
                    </Grid.Col>
                    
                    <Grid.Col span={4} >
                        <Box >
                            <Particles id="tsparticles" init={particlesInit} loaded={particlesLoaded} style={{ width: 'auto !important', zIndex: -5 }}
                            options={{
                                fpsLimit: 120,
                                color: ["#03dac6", "#fac561", "#000000"],
                                connectParticles: true,
                                interactivity: {
                                    events: {
                                        onClick: {
                                            enable: true,
                                            mode: "push",
                                        },
                                        onHover: {
                                            enable: true,
                                            mode: "repulse",
                                        },
                                        resize: true,
                                    },
                                    modes: {
                                        push: {
                                            quantity: 4,
                                        },
                                        repulse: {
                                            distance: 100,
                                            duration: 0.4,
                                        },
                                    },
                                },
                                particles: {
                                    color: {
                                        value: ["#faebd7", "#03dac6", "#fac561"],
                                    },
                                    links: {
                                        color: ["#faebd7", "#03dac6", "#fac561"],
                                        distance: 150,
                                        enable: true,
                                        opacity: 0.5,
                                        width: 1,
                                    },
                                    collisions: {
                                        enable: true,
                                    },
                                    move: {
                                        direction: "none",
                                        enable: true,
                                        outModes: {
                                            default: "bounce",
                                        },
                                        random: false,
                                        speed: 6,
                                        straight: false,
                                    },
                                    number: {
                                        density: {
                                            enable: true,
                                            area: 800,
                                        },
                                        value: 80,
                                    },
                                    opacity: {
                                        value: 0.5,
                                    },
                                    shape: {
                                        type: "circle",
                                    },
                                    size: {
                                        value: { min: 1, max: 5 },
                                    },
                                },
                                detectRetina: true,
                            }}
                            />
                        </Box>
                    </Grid.Col>

                </Grid>
            </Box>
        </MantineProvider>
    );
}

export default Landing;
