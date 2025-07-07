import React from 'react';
import { Link } from 'react-router-dom';
import { getPlayerImage } from "services/helpers.js";
import 'styles/tailwind.css';

const SubSpotlight = ({ topByWinrateRanking }) => {
  return (
    <section className="max-20 sm:mx-auto my-12 p-8 bg-gradient-to-r from-green-600 to-green-800 text-white rounded-lg max-w-screen-xl shadow-lg">
      <h2 className="text-4xl font-extrabold mb-6 text-center">Jugadores Play2Win</h2>
      <p className="text-xl mb-8 text-center">
        Estos jugadores se destacan por su winrate, ganándose el título de "Play2Win", jugar para ganar.
      </p>
      <div className="flex flex-wrap justify-center gap-6">
        {topByWinrateRanking.map((ranking, index) => {
          let winrateGradient;
          let nameGradient;

          // Gradients for Winrate and Name
          switch (index) {
            case 0:
              winrateGradient = "bg-gradient-to-r from-yellow-400 to-yellow-500";
              nameGradient = "bg-gradient-to-r from-yellow-400 to-yellow-500";
              break;
            case 1:
              winrateGradient = "bg-gradient-to-r from-gray-300 to-gray-500";
              nameGradient = "bg-gradient-to-r from-gray-300 to-gray-500";
              break;
            case 2:
              winrateGradient = "bg-gradient-to-r from-orange-400 to-orange-600";
              nameGradient = "bg-gradient-to-r from-orange-400 to-orange-600";
              break;
            case 3:
              winrateGradient = "bg-gradient-to-r from-pink-400 to-pink-600";
              nameGradient = "bg-gradient-to-r from-pink-400 to-pink-600";
              break;
            case 4:
              winrateGradient = "bg-gradient-to-r from-blue-400 to-blue-600";
              nameGradient = "bg-gradient-to-r from-blue-400 to-blue-600";
              break;
            default:
              winrateGradient = "bg-gradient-to-r from-gray-600 to-gray-800";
              nameGradient = "bg-gradient-to-r from-gray-600 to-gray-800";
          }

          return (
            <div
              key={ranking.player.id}
              className="group relative w-full sm:w-1/2 md:w-1/4 lg:w-1/5 bg-gray-800 rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-all duration-300">
              <Link to={`/players/${ranking.player.id}`} className="block text-white">
                {/* Player Image */}
                <img
                  src={getPlayerImage(ranking.player.photo)}
                  alt={`${ranking.player.first_name} ${ranking.player.last_name}`}
                  className="w-full h-48 object-cover rounded-t-lg group-hover:scale-105 transition-transform duration-300"
                />
                {/* Player Info */}
                <div className="p-4">
                  <h3 className={`text-xl font-extrabold text-transparent bg-clip-text ${nameGradient}`}>
                    {ranking.player.first_name} {ranking.player.last_name}
                  </h3>
                  {ranking.alias && (
                    <p className="text-sm italic text-gray-300">{`"${ranking.alias}"`}</p>
                  )}
                  <p className="mt-2 text-sm">
                    <strong>Partidos Jugados:</strong> {ranking.matches_played}
                  </p>
                  <p
                    className={`text-2xl font-bold mt-4 text-transparent bg-clip-text ${winrateGradient}`}>
                    {ranking.winrate}%
                  </p>
                </div>
                {/* Ribbon for Ranking */}
                {index < 5 && (
                  <div
                    className="absolute top-0 right-0 px-3 py-1 text-sm font-bold text-white bg-gradient-to-r from-red-500 to-red-700 rounded-bl-lg">
                    #{index + 1}
                  </div>
                )}
              </Link>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default SubSpotlight;
