import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getSingleMatches,
  getDoubleMatches,
  getPlayers,
  deleteMatch,
  checkMatchCountIntegrity,
  getCurrentSeason,
  getSeasons,
} from "services/api.js";
import AdminHeader from "components/admin/AdminHeader";
import AdminFooter from "components/admin/AdminFooter";
import ConfirmationModal from "components/admin/ConfirmationModal";
import AlertModal from "components/admin/AlertModal";
import { Spinner, Button, Select } from "flowbite-react";
import "styles/tailwind.css";

function AdminMatchList() {
  const [singleMatches, setSingleMatches] = useState([]);
  const [doubleMatches, setDoubleMatches] = useState([]);
  const [players, setPlayers] = useState({});
  const [currentSinglesPage, setCurrentSinglesPage] = useState(1);
  const [currentDoublesPage, setCurrentDoublesPage] = useState(1);
  const [totalSinglesPages, setTotalSinglesPages] = useState(1);
  const [totalDoublesPages, setTotalDoublesPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [alertData, setAlertData] = useState({ isOpen: false, type: "success", message: "" });
  const [matchToDelete, setMatchToDelete] = useState(null);
  const [matchToDeleteType, setMatchToDeleteType] = useState(null);
  const [seasons, setSeasons] = useState([]);
  const [selectedSeason, setSelectedSeason] = useState(null);

  const matchesPerPage = 20;

  const fetchSeasons = async () => {
    try {
      const allSeasons = await getSeasons(1, 100);
      setSeasons(allSeasons.results);
      if (allSeasons.count > 0) {
        setSelectedSeason(allSeasons.results[0].id);
      }
    } catch (error) {
      console.error("Error fetching seasons:", error);
    }
  };

  const fetchPlayers = async (playerIds) => {
    try {
      const players = await getPlayers(1, 100);
      for (const player of players.results) {
        setPlayers((prev) => ({ ...prev, [player.id]: `${player.first_name} ${player.last_name}` }));
      }
    } catch (error) {
      console.error("Error fetching players:", error);
    }
  };

  const fetchMatches = async (seasonId) => {
    if (!seasonId) return;
    setLoading(true);
    try {
      const singleResult = await getSingleMatches(currentSinglesPage, matchesPerPage, seasonId);
      const singlePlayerIds = singleResult.results.flatMap((match) => [match.player1, match.player2]);
      await fetchPlayers(singlePlayerIds);
      setSingleMatches(singleResult.results);
      setTotalSinglesPages(Math.ceil(singleResult.count / matchesPerPage));

      const doubleResult = await getDoubleMatches(currentDoublesPage, matchesPerPage, seasonId);
      const doublePlayerIds = doubleResult.results.flatMap((match) => [
        match.team1_player1,
        match.team1_player2,
        match.team2_player1,
        match.team2_player2,
      ]);
      await fetchPlayers(doublePlayerIds);
      setDoubleMatches(doubleResult.results);
      setTotalDoublesPages(Math.ceil(doubleResult.count / matchesPerPage));
    } catch (error) {
      console.error("Error fetching matches:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteClick = (match, type) => {
    setMatchToDelete(match);
    setMatchToDeleteType(type);
    setIsModalOpen(true);
  };

  const handleConfirmDelete = async () => {
    if (matchToDelete) {
      try {
        await deleteMatch(matchToDelete.id, matchToDeleteType);
        fetchMatches(selectedSeason);
        setAlertData({
          isOpen: true,
          type: "success",
          message: "El partido ha sido eliminado correctamente.",
        });
      } catch (error) {
        console.error("Error deleting match:", error);
        setAlertData({
          isOpen: true,
          type: "error",
          message: "Hubo un error al eliminar el partido.",
        });
      } finally {
        setIsModalOpen(false);
        setMatchToDelete(null);
      }
    }
  };

  const handleCancelDelete = () => {
    setIsModalOpen(false);
    setMatchToDelete(null);
  };

  const handleMatchCountCheck = async () => {
    try {
      const result = await checkMatchCountIntegrity(selectedSeason);
      const messages = Object.values(result).join("\n");
      setAlertData({
        isOpen: true,
        type: "advice",
        message: messages,
      });
    } catch (error) {
      console.error("Error checking match count integrity:", error);
      setAlertData({
        isOpen: true,
        type: "error",
        message: "Error al verificar la integridad del conteo de partidos.",
      });
    }
  };

  useEffect(() => {
    fetchSeasons();
  }, []);

  useEffect(() => {
    if (selectedSeason) {
      fetchMatches(selectedSeason);
    }
  }, [selectedSeason, currentSinglesPage, currentDoublesPage]);

  const handleSeasonChange = (event) => {
    setSelectedSeason(event.target.value);
  };

  const getPlayerName = (id) => players[id] || "N/A";

  const navigate = useNavigate();

  const renderMatches = (matches, type) => (
    <div className="mb-8">
      <h3 className="text-2xl font-bold mb-4">{type === 'singles' ? 'Partidos Individuales' : 'Partidos Dobles'}</h3>
      <table className="table-auto w-full border-collapse border border-gray-300 text-center text-sm">
        <thead>
          <tr className="bg-gray-200">
            <th className="border border-gray-300 px-4 py-2">Fecha</th>
            <th className="border border-gray-300 px-4 py-2">{type === 'singles' ? 'Jugador 1' : 'Equipo 1'}</th>
            <th className="border border-gray-300 px-4 py-2">{type === 'singles' ? 'Jugador 2' : 'Equipo 2'}</th>
            <th className="border border-gray-300 px-4 py-2">Juegos ganados</th>
            <th className="border border-gray-300 px-4 py-2">{type === 'singles' ? 'Ganador' : 'Ganadores'}</th>
            <th className="border border-gray-300 px-4 py-2">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {matches.length > 0 ? (
            matches.map((match) => (
              <tr key={match.id} className="hover:bg-gray-100">
                <td className="border border-gray-300 px-4 py-2">{new Date(match.date).toLocaleString()}</td>
                <td className="border border-gray-300 px-4 py-2">
                  {type === 'singles'
                    ? getPlayerName(match.player1)
                    : `${getPlayerName(match.team1_player1)} / ${getPlayerName(match.team1_player2)}`}
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  {type === 'singles'
                    ? getPlayerName(match.player2)
                    : `${getPlayerName(match.team2_player1)} / ${getPlayerName(match.team2_player2)}`}
                </td>
                <td className="border border-gray-300 px-4 py-2">
                  {type === 'singles'
                    ? `${match.player1_games}-${match.player2_games}`
                    : `${match.team1_games}-${match.team2_games}`}
                </td>
                <td className="border border-gray-300 px-4 py-2">{type === 'singles' ? getPlayerName(match.winner) : getPlayerName(match.winner_1) + " | " + getPlayerName(match.winner_2)}</td>
                <td className="border border-gray-300 px-4 py-2">
                  <div className="flex justify-center space-x-2">
                    <a
                      href={`/admin/matches/${type}/edit/${match.id}`}
                      className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                    >
                      Editar
                    </a>
                    <button
                      onClick={() => handleDeleteClick(match, type)}
                      className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                    >
                      Eliminar
                    </button>
                  </div>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" className="text-center text-gray-500 py-4">
                No hay partidos registrados.
              </td>
            </tr>
          )}
        </tbody>
      </table>
      <div className="flex justify-between mt-4">
        <button
          onClick={() => (type === 'singles' ? setCurrentSinglesPage : setCurrentDoublesPage)((prev) => Math.max(prev - 1, 1))}
          disabled={type === 'singles' ? currentSinglesPage === 1 : currentDoublesPage === 1}
          className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300"
        >
          Anterior
        </button>
        <span className="text-gray-600">
          {`Página ${
            type === 'singles' ? currentSinglesPage : currentDoublesPage
          } de ${type === 'singles' ? totalSinglesPages : totalDoublesPages}`}
        </span>
        <button
          onClick={() => (type === 'singles' ? setCurrentSinglesPage : setCurrentDoublesPage)((prev) => prev + 1)}
          disabled={type === 'singles' ? currentSinglesPage === totalSinglesPages : currentDoublesPage === totalDoublesPages}
          className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300"
        >
          Siguiente
        </button>
      </div>
    </div>
  );

  return (
    <div className="bg-white min-h-screen text-gray-800 flex flex-col">
      <ConfirmationModal
        isOpen={isModalOpen}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        message="Seguro que quieres borrar este partido? Esta acción no se puede deshacer."
        deleteItem="Borrar Partido"
        cancelItem="Cancelar"
      />

      <AlertModal
        isOpen={alertData.isOpen}
        onClose={() => setAlertData((prev) => ({ ...prev, isOpen: false }))}
        type={alertData.type}
        message={alertData.message}
      />
      <AdminHeader />
      <main className="container mx-auto px-4 py-8 flex-grow">
        <h2 className="text-center text-4xl font-bold mb-8">Lista de Partidos</h2>

        <div className="mb-4">
          <label className="block text-gray-700 font-bold mb-2">Seleccionar Temporada:</label>
          <Select onChange={handleSeasonChange} value={selectedSeason}>
            {seasons.map((season) => (
              <option key={season.id} value={season.id}>
                {season.name}
              </option>
            ))}
          </Select>
        </div>


        {loading ? (
          <div className="flex justify-center items-center">
            <Spinner size="xl" />
          </div>
        ) : (
          <>
            <Button
              color="blue"
              onClick={() => navigate({ pathname: `/admin/matches/singles/add` })}
              className="font-medium"
            >
              Agregar Partido Individual
            </Button>
            <Button
              color="blue"
              onClick={() => navigate({ pathname: `/admin/matches/doubles/add` })}
              className="font-medium"
            >
              Agregar Partido Doble
            </Button>
            {singleMatches.length === 0 && doubleMatches.length === 0 ? (
              <p className="text-center text-gray-500">No hay partidos registrados para esta temporada.</p>
            ) : (
              <>
                <Button color={'green'} onClick={handleMatchCountCheck} className="mb-4">Comprobar match_count</Button>
                <Button color="green" onClick={() => fetchMatches(selectedSeason)} className="mb-4">
                  Refrescar Partidos
                </Button>
                {renderMatches(singleMatches, "singles")}
                {renderMatches(doubleMatches, "doubles")}
              </>
            )}
          </>
        )}
      </main>
      <AdminFooter />
    </div>
  );
}

export default AdminMatchList;
