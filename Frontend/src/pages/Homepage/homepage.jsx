import React from 'react';
// import particlesConfig from '../../components/config/particles'; // This can stay if you use a separate config file
// import Particles from "react-tsparticles"; // You can import Particles directly if not using ParticlesComponent
import SearchBar from '../../components/SearchBar/searchbar';
import ParticlesComponent from '../../components/config/particles'; // Import your ParticlesComponent

const HomePage = () => {
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh',
            position: 'relative',
            overflow: 'hidden'
        }}>
            <ParticlesComponent id="particles" />
            <h1 style={{ position: 'relative', zIndex: 2 }}>Welcome to KeenKaraoke</h1>
            <div style={{ position: 'relative', zIndex: 2 }}>
                <SearchBar />
            </div>
        </div>
    );
};

export default HomePage;
