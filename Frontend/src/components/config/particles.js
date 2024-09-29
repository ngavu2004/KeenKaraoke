import Particles, { initParticlesEngine } from "@tsparticles/react";
import { useEffect, useMemo, useState } from "react";
import { loadSlim } from "@tsparticles/slim";

const ParticlesComponent = (props) => {
    const [init, setInit] = useState(false);

    useEffect(() => {
        initParticlesEngine(async (engine) => {
            await loadSlim(engine);
        }).then(() => {
            setInit(true);
        });
    }, []);

    const particlesLoaded = (container) => {
        console.log(container);
    };

    const options = useMemo(
        () => ({
            background: {
                color: {
                    value: "#000000", // Dark background color
                },
            },
            fpsLimit: 120,
            interactivity: {
                events: {
                    onClick: {
                        enable: true,
                        mode: "push", // Change interaction mode
                    },
                    onHover: {
                        enable: true,
                        mode: 'repulse',
                    },
                },
                modes: {
                    push: {
                        quantity: 4, // Number of particles to push on click
                    },
                    repulse: {
                        distance: 100,
                        duration: 0.4,
                    },
                },
            },
            particles: {
                color: {
                    value: "#FF69B4", // Heart-themed color
                },
                links: {
                    color: "#FF69B4", // Link color to match heart theme
                    distance: 150,
                    enable: true,
                    opacity: 0.5,
                    width: 2,
                },
                move: {
                    direction: "none",
                    enable: true,
                    outModes: {
                        default: "bounce",
                    },
                    random: true,
                    speed: 2, // Increased speed for a more dynamic effect
                    straight: false,
                },
                number: {
                    density: {
                        enable: true,
                        area: 800, // Adjusted density for more particles
                    },
                    value: 150,
                },
                opacity: {
                    value: 0.5, // Adjust opacity for a softer look
                },
                shape: {
                    type: ["circle", "heart"], // Use both circles and heart shapes
                },
                size: {
                    value: { min: 5, max: 10 }, // Increased size for better visibility
                },
            },
            detectRetina: true,
        }),
        [],
    );

    return <Particles id={props.id} init={particlesLoaded} options={options} />;
};

export default ParticlesComponent;
