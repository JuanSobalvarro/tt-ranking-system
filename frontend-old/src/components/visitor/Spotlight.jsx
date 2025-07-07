import React from "react";
import { Carousel } from "flowbite-react";
import "styles/tailwind.css";
import { getPlayerImage, getAge } from "services/helpers.js";

const Spotlight = ({ topPlayersRanking }) => {
  if (!topPlayersRanking || topPlayersRanking.length === 0) {
    return <p className="text-center text-white py-5">No hay jugadores destacados.</p>;
  }

  const getGradient = (index) => {
    switch (index) {
      case 0:
        return "bg-gradient-to-r from-yellow-300 to-yellow-400"; // Gold
      case 1:
        return "bg-gradient-to-r from-gray-300 to-gray-400"; // Silver
      case 2:
        return "bg-gradient-to-r from-orange-300 to-orange-400"; // Bronze
      default:
        return "bg-gradient-to-r from-gray-200 to-gray-300"; // Default
    }
  };

  console.log(topPlayersRanking);

  return (
    <div className="mx-auto my-12 w-[95%] max-w-7xl bg-gradient-to-r from-gray-800 via-gray-900 to-black rounded-lg overflow-hidden relative">
      {/* Title */}
      <div className="absolute top-2 md:top-10 left-1/2 transform -translate-x-1/2 text-center text-white z-10">
        <h2 className="text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 via-emerald-400 to-emerald-500">
          Nuestras Estrellas
        </h2>
      </div>

      <Carousel indicators className="h-[500px] mt-20 md:mt-5">
        {topPlayersRanking.map((ranking, index) => (
          <div key={ranking.player.id} className="flex flex-col md:flex-row items-center md:items-stretch h-full">
            {/* Player Image */}
            <div className="w-full md:w-1/3 h-1/2 md:h-full flex justify-center items-center">
              <div className="relative w-[200px] h-[200px] md:w-[300px] md:h-[300px] overflow-hidden rounded-lg shadow-lg">
                <img
                  src={getPlayerImage(ranking.player.photo) || "/placeholder.png"}
                  alt={`Imagen de ${ranking.player.first_name || "Jugador"}`}
                  className="w-full h-full object-cover"
                />
              </div>
            </div>

            {/* Player Info */}
            <div className="w-full md:w-2/3 flex flex-col justify-center p-4 md:p-6 text-white">
              <h3
                className={`text-xl md:text-3xl font-bold text-transparent bg-clip-text ${getGradient(
                  index
                )}`}
              >
                {ranking.player.first_name} {ranking.player.last_name}
              </h3>
              <p className="text-sm md:text-lg italic text-gray-300">
                {ranking.player.alias || ""}
              </p>
              <div className="mt-4 flex items-center">
                {/* Rank */}
                <span
                  className={`text-4xl md:text-5xl font-bold text-transparent bg-clip-text ${getGradient(
                    index
                  )}`}
                >
                  #{index + 1}
                </span>
                {/* Details */}
                <div className="ml-4 border-l border-gray-300 pl-4">
                  <p className="text-sm md:text-lg font-bold">
                    {ranking.player.nationality ? (
                      <img
                        src={`https://flagsapi.com/${ranking.player.nationality}/flat/32.png`}
                        alt={`Bandera de ${ranking.player.nationality}`}
                        className="inline-block"
                      />
                    ) : (
                      "N/D"
                    )}{" "}
                    {ranking.player.nationality || "N/D"}
                  </p>
                  <p className="text-sm md:text-lg">
                    {getAge(ranking.player.date_of_birth) ? (
                      <>
                        {getAge(ranking.player.date_of_birth)}{" "}
                        <span className="text-xs md:text-sm">años</span>
                      </>
                    ) : (
                      " "
                    )}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </Carousel>
    </div>
  );
};

export default Spotlight;
