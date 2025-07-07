import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getHomeData } from 'services/api.js';
import { motion } from 'framer-motion';
import { Button } from 'flowbite-react';
import Header from 'components/visitor/Header.jsx';
import Footer from 'components/visitor/Footer.jsx';
import 'styles/tailwind.css';
import 'styles/pingpong.css'
import Spotlight from "components/visitor/Spotlight.jsx";
import SubSpotlight from "components/visitor/SubSpotlight.jsx";
import RankingTable from "components/visitor/RankingTable.jsx";
import SeasonDescription from "components/visitor/SeasonDescription.jsx";

function Home() {
  const [matchesPlayed, setMatchesPlayed] = useState(0);
  const [topPlayers, setTopPlayers] = useState([]);
  const [topByWinrate, setTopByWinrate] = useState([]);
  const [ranking, setRanking] = useState([]);
  const [currentSeason, setCurrentSeason] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getHomeData();
        console.log(data);
        setMatchesPlayed(data.matchesPlayed);
        setTopPlayers(data.topPlayers);
        setTopByWinrate(data.topByWinrate);
        setRanking(data.ranking);
        setCurrentSeason(data.currentSeason);
      } catch (error) {
        console.error('Error fetching home data:', error);
      }
    };

    fetchData();
  }, []);

  // console.log(topPlayers);

  return (
    <div className='bg-gray-900'>
      <Header />

      {/* Hero Section with dynamic table tennis-inspired background */}
      <motion.section
          className="hero-section bg-gradient-to-r from-green-600 via-black to-green-900 text-white text-center relative overflow-hidden"
          initial={{opacity: 0}}
          animate={{opacity: 1}}
          transition={{duration: 1}}
      >
        {/* Animated Lights mimicking the fast movement of a ping-pong ball */}
        <div className="absolute inset-0 bg-opacity-50 bg-black z-0"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-green-900 via-teal-900 to-green-600 opacity-10 animate-pulse z-0"></div>


        <motion.div
            className="text-center py-16 relative z-10"
            initial={{opacity: 0, scale: 0.9}}
            animate={{opacity: 1, scale: 1}}
            transition={{duration: 1}}
        >
          <h1 className="text-5xl font-extrabold tracking-wide">
            Bienvenido al Sistema de Clasificación de Tenis de Mesa 🏓
          </h1>
          <p className="text-lg mt-6">
            Sigue el rendimiento de los jugadores y consulta las últimas clasificaciones.
          </p>

          <motion.div
              className="mt-8 flex justify-center gap-4"
              initial={{opacity: 0.5, y: 10}}
              animate={{opacity: 1, y: 0}}
              transition={{delay: 1}}
          >
              <Button gradientDuoTone="greenToBlue" as={Link} to="/players">
                Ver Jugadores
              </Button>
              <Button gradientDuoTone="purpleToBlue" as={Link} to="/matches">
                Ver Partidos
              </Button>
              <Button gradientDuoTone="greenToBlue" as={Link} to="/seasons">
                Ver Temporadas
              </Button>
          </motion.div>
        </motion.div>
      </motion.section>

      {/* Matches Played Bar */}
      <motion.div
        className="bg-green-500 text-white py-3"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1 }}
      >
        <div className="text-center">
          <motion.div
            className="text-lg font-semibold"
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 100 }}
          >
            🏆 Total Partidos Jugados {currentSeason ? currentSeason.name : ''}: {matchesPlayed}
          </motion.div>
        </div>
      </motion.div>

      {/* Spotlight and Ranking Sections */}
        <motion.div
            initial={{opacity: 0}}
            animate={{opacity: 1}}
            transition={{duration: 1, delay: 0.3}}
        >
            <Spotlight topPlayersRanking={topPlayers}/>


            <SubSpotlight topByWinrateRanking={topByWinrate}/>
            <motion.div
                className='container mx-auto my-12 text-center text-white px-6'
                initial={{opacity: 0, scale: 0.9}}
                animate={{opacity: 1, scale: 1}}
                transition={{duration: 1}}
            >
                <SeasonDescription season={currentSeason}/>
            </motion.div>
            <RankingTable ranking={ranking} title="🏆 Top 20 Jugadores 🏆"/>
        </motion.div>

        {/* Description Section */}
        <motion.div
            className="container mx-auto my-12 text-center text-white px-6"
            initial={{opacity: 0, y: 20}}
            animate={{opacity: 1, y: 0}}
            transition={{duration: 1}}
      >
        <h2 className="text-3xl font-bold mb-6">📊 Sobre el sistema de Clasificación</h2>
        <p className="text-xl mb-6">
          Nuestro sistema de clasificación de tenis de mesa está diseñado para ofrecer una representación precisa
          y dinámica del rendimiento de los jugadores a lo largo del tiempo. Cada jugador acumula puntos en
          función de los resultados de sus victorias.
        </p>
        <p className="text-xl mb-6">
          Ya sean principiantes, avanzados o profesionales, todos pueden participar en nuestro grupo y ser
          registrados/as en nuestra clasificación.
        </p>
      </motion.div>


      <Footer />
    </div>
  );
}

export default Home;
