import React from 'react';
import { Link } from 'react-router-dom';
import 'styles/tailwind.css';
import { Table } from 'flowbite-react';
import { getPlayerImage } from "services/helpers.js";

const RankingTable = ({ ranking, title }) => {
  // Sort ranking in descending order
  ranking.sort((a, b) => b.ranking - a.ranking);

  return (
    <div className="container mx-auto my-12 px-4">
      <h2 className="text-center text-4xl font-extrabold mb-8 text-gray-100">
        {title}
      </h2>
      <div className="overflow-x-auto shadow-lg rounded-lg border border-gray-700 bg-gray-800">
        <Table striped hoverable>
          <thead className="bg-gray-700">
            <tr>
              <th className="py-3 px-6 text-center text-gray-300">Posición</th>
              <th className="py-3 px-6 text-left text-gray-300">Jugador</th>
              <th className="py-3 px-6 text-center text-gray-300">Nacionalidad</th>
              <th className="py-3 px-6 text-center text-gray-300">Puntos</th>
              <th className="py-3 px-6 text-center text-gray-300">Partidos</th>
              <th className="py-3 px-6 text-center text-gray-300">Victorias</th>
              <th className="py-3 px-6 text-center text-gray-300">% Victorias</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            {ranking.map((rank, index) => (
              <tr
                key={rank.player.id}
                className={`${
                  index % 2 === 0 ? "bg-gray-800" : "bg-gray-700"
                } hover:bg-gray-600 transition-all duration-300 text-gray-200`}
              >
                {/* Position */}
                <td
                  className={`py-3 px-6 text-center font-bold ${
                    index < 3
                      ? "text-yellow-400"
                      : index < 5
                      ? "text-gray-400"
                      : "text-gray-300"
                  }`}
                >
                  {index + 1}
                </td>
                {/* Player Info */}
                <td className="py-3 px-6 flex items-center">
                  <Link
                    to={`/players/${rank.player.id}`}
                    className="flex items-center no-underline text-gray-200 hover:text-green-400"
                  >
                    <img
                      src={getPlayerImage(rank.player.photo)}
                      alt={`${rank.player.first_name} ${rank.player.last_name}`}
                      className="w-12 h-12 rounded-full mr-4 object-cover shadow-md"
                    />
                    <div>
                      <strong className="block text-lg">{`${rank.player.first_name} ${rank.player.last_name}`}</strong>
                      {rank.player.alias && (
                        <span className="text-sm text-gray-400">{`"${rank.player.alias}"`}</span>
                      )}
                    </div>
                  </Link>
                </td>
                {/* Nationality */}
                <td className="py-3 px-6 text-center">
                  {rank.player.nationality ? (
                    <div className="flex justify-center items-center gap-2">
                      <img
                        src={`https://flagsapi.com/${rank.player.nationality}/flat/32.png`}
                        alt={`Bandera de ${rank.player.nationality}`}
                        className="inline-block"
                      />
                      <span className="text-sm">{rank.player.nationality}</span>
                    </div>
                  ) : (
                    <span className="text-gray-500">N/D</span>
                  )}
                </td>
                {/* Points */}
                <td className="py-3 px-6 text-center font-medium text-gray-300">
                  {rank.ranking}
                </td>
                {/* Matches Played */}
                <td className="py-3 px-6 text-center">{rank.matches_played}</td>
                {/* Victories */}
                <td className="py-3 px-6 text-center text-green-400 font-bold">
                  {rank.victories}
                </td>
                {/* Winrate */}
                <td
                  className={`py-3 px-6 text-center font-bold ${
                    rank.winrate >= 80
                      ? "text-green-400"
                      : rank.winrate >= 50
                      ? "text-yellow-400"
                      : "text-red-400"
                  }`}
                >
                  {rank.winrate}%
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </div>
  );
};

export default RankingTable;
