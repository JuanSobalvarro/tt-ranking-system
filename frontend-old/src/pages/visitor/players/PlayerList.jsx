import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getPlayers } from 'services/api.js';
import Header from 'components/visitor/Header';
import Footer from 'components/visitor/Footer';
import 'styles/tailwind.css';

function PlayerList() {
  const [players, setPlayers] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchPlayers = async (page = 1) => {
    try {
      const playersPerPage = 12;
      const resultPlayers = await getPlayers(page, playersPerPage);
      setPlayers(resultPlayers.results);
      setTotalPages(Math.ceil(resultPlayers.count / playersPerPage)); // Use playersPerPage for total page calculation
    } catch (error) {
      console.error('Error fetching players:', error);
    }
  };

  useEffect(() => {
    fetchPlayers(currentPage);
  }, [currentPage]);

  const handleNextPage = () => {
    if (currentPage < totalPages) setCurrentPage((prevPage) => prevPage + 1);
  };

  const handlePrevPage = () => {
    if (currentPage > 1) setCurrentPage((prevPage) => prevPage - 1);
  };

  return (
    <div className="bg-gradient-to-r from-gray-800 via-gray-900 to-black min-h-screen text-white flex flex-col">
      <Header />
      <main className="container mx-auto px-4 py-8 flex-grow">
        <h2 className="text-center text-4xl font-bold mb-8">
          Lista de Jugadores
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {players.map((player) => (
            <Link key={player.id} to={`/players/${player.id}`}>
              <div className="bg-gray-700 rounded-lg shadow-lg overflow-hidden flex flex-col items-center">
                {/* Player Image */}
                <img
                  src={player.photo ? player.photo : '/assets/images/defaultPlayer.png'}
                  alt={`${player.first_name} ${player.last_name}`}
                  className="w-48 h-48 object-cover rounded-full mt-6"
                />
                {/* Player Info */}
                <div className="p-6 h-32 text-center flex flex-col justify-between">
                  <h5 className="text-xl font-bold">{player.first_name} {player.last_name}</h5>
                  <p className="text-sm italic text-gray-300">{player.alias || ''}</p>
                  {/*<p className="mt-2 text-sm text-gray-400">Ranking: <span className="font-semibold">{player.ranking || 'N/A'}</span></p>*/}
                </div>
              </div>
            </Link>
          ))}

        </div>

        {/* Pagination */}
        <div className="mt-8 flex justify-between items-center">
          <button
            onClick={handlePrevPage}
            disabled={currentPage === 1}
            className={`px-4 py-2 rounded ${currentPage === 1 ? 'bg-gray-600' : 'bg-emerald-500 hover:bg-emerald-600'} text-white`}
          >
            Anterior
          </button>
          <span className="text-lg font-medium">
            Página {currentPage} de {totalPages}
          </span>
          <button
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
            className={`px-4 py-2 rounded ${currentPage === totalPages ? 'bg-gray-600' : 'bg-emerald-500 hover:bg-emerald-600'} text-white`}
          >
            Siguiente
          </button>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default PlayerList;
