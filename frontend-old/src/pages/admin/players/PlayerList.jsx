import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "flowbite-react";
import AdminHeader from "components/admin/AdminHeader";
import AdminFooter from "components/admin/AdminFooter";
import { getRankings, getPlayers, deletePlayer, rankings_integrity } from "services/api.js";
import ConfirmationModal from "components/admin/ConfirmationModal.jsx";
import AlertModal from "components/admin/AlertModal.jsx"; // Add this for feedback
import "styles/tailwind.css";

function AdminPlayerList() {
  const [players, setPlayers] = useState([]);
  const [rankings, setRankings] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [isIntegrityModalOpen, setIsIntegrityModalOpen] = useState(false);
  const [integrityResult, setIntegrityResult] = useState(null);
  const [playerToDelete, setPlayerToDelete] = useState(null);
  const navigate = useNavigate();

  const fetchPlayers = async (page = 1) => {
    try {
      const result = await getPlayers(page);
      const resultRankings = await getRankings();
      setRankings(resultRankings);
      setPlayers(result.results);
      setTotalPages(Math.ceil(result.count / 10));
    } catch (error) {
      console.error("Error fetching players:", error);
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

  const handleDeletePlayer = (playerId) => {
    setPlayerToDelete(playerId);
    setIsDeleteModalOpen(true);
  };

  const handleConfirmDelete = async () => {
    try {
      await deletePlayer(playerToDelete);
      fetchPlayers(currentPage);
      setIsDeleteModalOpen(false);
    } catch (error) {
      console.error("Error deleting player:", error);
    }
  };

  const handleCancelDelete = () => {
    setIsDeleteModalOpen(false);
  };

  const handleRankingsIntegrityCheck = async () => {
  try {
    const result = await rankings_integrity();
    if (result && result.status === 200) {
      // Extract the list of verified players from the response
      const verifiedPlayers = Object.values(result.data).map((message) => message);
      setIntegrityResult({
        success: true,
        message: "La integridad de los rankings ha sido verificada correctamente.",
        verifiedPlayers: verifiedPlayers, // Add the list of verified players
      });
    } else {
      setIntegrityResult({
        success: false,
        error: "Failed to check rankings integrity.",
      });
    }
    setIsIntegrityModalOpen(true);
  } catch (error) {
    console.error("Error checking rankings integrity:", error);
    setIntegrityResult({
      success: false,
      error: "Failed to check rankings integrity.",
    });
    setIsIntegrityModalOpen(true);
  }
};

  return (
    <div>
      <AdminHeader />
      <main className="container mx-auto px-4 py-8">
        {/* Delete Confirmation Modal */}
        <ConfirmationModal
          isOpen={isDeleteModalOpen}
          onConfirm={handleConfirmDelete}
          onCancel={handleCancelDelete}
          message="¿Seguro que quieres borrar este jugador? Esta acción no se puede deshacer."
          deleteItem="Borrar jugador"
          cancelItem="Cancelar"
        />

        <AlertModal
          isOpen={isIntegrityModalOpen}
          message={
            integrityResult?.error
              ? integrityResult.error
              : integrityResult?.success
              ? integrityResult.message
              : "La integridad de los rankings ha sido verificada correctamente."
          }
          type={integrityResult?.error ? "error" : "success"}
          onClose={() => setIsIntegrityModalOpen(false)}
        >
          {integrityResult?.success && integrityResult.verifiedPlayers && (
            <div className="mt-4">
              <h4 className="text-lg font-semibold">Jugadores verificados:</h4>
              <ul className="list-disc list-inside">
                {integrityResult.verifiedPlayers.map((player, index) => (
                  <li key={index} className="text-gray-700">
                    {player}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </AlertModal>

        <h2 className="text-3xl font-bold mb-6">Lista de Jugadores</h2>

        {/* Rankings Integrity Check Button */}
        <Button
          onClick={handleRankingsIntegrityCheck}
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded mb-6"
        >
          Verificar integridad de rankings
        </Button>

        {/* Add New Player Button */}
        <Link
          to="/admin/players/add"
          className="inline-block bg-green-500 text-white px-6 py-3 rounded hover:bg-green-600 mb-6"
        >
          Agregar Nuevo Jugador
        </Link>

        {/* Player Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {players.map((player) => (
            <div
              key={player.id}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-200"
            >
              <img
                src={player.photo ? player.photo : "/assets/images/defaultPlayer.png"}
                alt={`${player.first_name} ${player.last_name}`}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h5 className="text-xl font-semibold">
                  {player.first_name} {player.last_name}
                </h5>
                <p className="text-gray-600">{player.alias}</p>
                <p className="text-gray-800 font-semibold">Ranking: {player.ranking}</p>
                <div className="mt-4 flex justify-between">
                  <Link
                    to={`/admin/players/edit/${player.id}`}
                    className="bg-yellow-400 text-white px-4 py-2 rounded hover:bg-yellow-500"
                  >
                    Editar
                  </Link>
                  <button
                    onClick={() => handleDeletePlayer(player.id)}
                    className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                  >
                    Eliminar
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Pagination Controls */}
        <div className="mt-8 flex justify-between">
          <button
            onClick={handlePrevPage}
            disabled={currentPage === 1}
            className={`px-4 py-2 rounded ${
              currentPage === 1 ? "bg-gray-400" : "bg-blue-500 hover:bg-blue-600"
            } text-white`}
          >
            Anterior
          </button>
          <span className="text-lg font-medium">
            Página {currentPage} de {totalPages}
          </span>
          <button
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
            className={`px-4 py-2 rounded ${
              currentPage === totalPages ? "bg-gray-400" : "bg-blue-500 hover:bg-blue-600"
            } text-white`}
          >
            Siguiente
          </button>
        </div>
      </main>
      <AdminFooter />
    </div>
  );
}

export default AdminPlayerList;
