import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  getSingleMatches,
  getDoubleMatches,
  getPlayers,
  getSeasons, // Add function to fetch seasons
} from "services/api.js";
import Header from "components/visitor/Header";
import Footer from "components/visitor/Footer";
import "styles/tailwind.css";
import { Spinner, Button, Select } from "flowbite-react";

function MatchList() {
  const [singleMatches, setSingleMatches] = useState([]);
  const [doubleMatches, setDoubleMatches] = useState([]);
  const [players, setPlayers] = useState({});
  const [seasons, setSeasons] = useState([]);
  const [selectedSeason, setSelectedSeason] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const matchesPerPage = 10;

  const fetchSeasons = async () => {
    try {
      const response = await getSeasons();
      setSeasons(response.results);
      if (response.results.length > 0) {
        setSelectedSeason(response.results[0].id);
      }
    } catch (error) {
      console.error("Error fetching seasons:", error);
    }
  };

  const fetchPlayers = async () => {
    try {
      const response = await getPlayers(1, 100);
      const playerData = response.results.reduce((acc, player) => {
        acc[player.id] = `${player.first_name} ${player.last_name}`;
        return acc;
      }, {});
      // console.log(playerData);
      setPlayers(playerData);
    } catch (error) {
      console.error("Error fetching players:", error);
    }
  };

  const fetchMatches = async () => {
    if (!selectedSeason) return;
    try {
      setLoading(true);
      const [singleResult, doubleResult] = await Promise.all([
        getSingleMatches(1, matchesPerPage, selectedSeason),
        getDoubleMatches(1, matchesPerPage, selectedSeason),
      ]);
      setSingleMatches(singleResult.results);
      setDoubleMatches(doubleResult.results);
    } catch (error) {
      console.error("Error fetching matches:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSeasons();
    fetchPlayers();
  }, []);

  useEffect(() => {
    fetchMatches();
  }, [selectedSeason]);

  const getPlayerName = (id) => players[id] || "N/A";

  const renderMatches = (matches, type) => (
    <div className="mb-8">
      <h3 className="text-xl md:text-2xl font-bold mb-4 text-center">
        {type === "singles" ? "Partidos Individuales" : "Partidos Dobles"}
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm md:text-base text-center border border-gray-300">
          <thead>
            <tr className="bg-gray-800 text-white">
              <th className="px-4 py-2">Fecha</th>
              <th className="px-4 py-2">{type === "singles" ? "Jugador 1" : "Equipo 1"}</th>
              <th className="px-4 py-2">{type === "singles" ? "Jugador 2" : "Equipo 2"}</th>
              <th className="px-4 py-2">Juegos ganados</th>
              <th className="px-4 py-2">{type === "singles" ? "Ganador" : "Ganadores"}</th>
              <th className="px-4 py-2">Detalles</th>
            </tr>
          </thead>
          <tbody>
            {matches.length > 0 ? (
              matches.map((match) => (
                <tr key={match.id} className="hover:bg-gray-700">
                  <td className="border px-4 py-2">{new Date(match.date).toLocaleString()}</td>
                  <td className="border px-4 py-2">
                    {type === "singles"
                      ? getPlayerName(match.player1)
                      : `${getPlayerName(match.team1_player1)} / ${getPlayerName(match.team1_player2)}`}
                  </td>
                  <td className="border px-4 py-2">
                    {type === "singles"
                      ? getPlayerName(match.player2)
                      : `${getPlayerName(match.team2_player1)} / ${getPlayerName(match.team2_player2)}`}
                  </td>
                  <td className="border px-4 py-2">
                    {type === "singles"
                      ? `${match.player1_games}-${match.player2_games}`
                      : `${match.team1_games}-${match.team2_games}`}
                  </td>
                  <td className="border px-4 py-2">
                    {type === "singles"
                      ? getPlayerName(match.winner)
                      : `${getPlayerName(match.winner_1)} | ${getPlayerName(match.winner_2)}`}
                  </td>
                  <td className="border px-4 py-2">
                    <Button
                      onClick={() => navigate(`/matches/${type}/${match.id}`)}
                      className="bg-blue-500 text-white hover:bg-blue-600"
                    >
                      Ver detalles
                    </Button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="text-gray-500 py-4 text-center">
                  No hay partidos registrados.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );

  return (
    <div className="bg-gradient-to-r from-gray-800 via-gray-900 to-black min-h-screen text-white flex flex-col">
      <Header />
      <main className="container mx-auto px-4 py-8 flex-grow">
        <h2 className="text-center text-3xl md:text-4xl font-bold mb-8">
          Lista de Partidos
        </h2>

        {/* Season Selector */}
        <div className="flex justify-center mb-6">
          <Select
            value={selectedSeason || ""}
            onChange={(e) => setSelectedSeason(e.target.value)}
            className="w-64 bg-gray-700 text-white"
          >
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
            {renderMatches(singleMatches, "singles")}
            {renderMatches(doubleMatches, "doubles")}
          </>
        )}
      </main>
      <Footer />
    </div>
  );
}

export default MatchList;
