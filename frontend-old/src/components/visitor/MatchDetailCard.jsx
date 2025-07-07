import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { TrophyIcon } from '@heroicons/react/24/solid';
import { Card, Badge } from 'flowbite-react';
import { getSingleMatch, getDoubleMatch, getMatchGames, getPlayer } from 'services/api';
import { getPlayerFullname } from "services/helpers.js";
import 'styles/tailwind.css';

function MatchDetailCard({ matchType }) {
  const { id } = useParams();
  const [match, setMatch] = useState(null);
  const [games, setGames] = useState([]);
  const [players, setPlayers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMatchDetails = async () => {
      try {
        setLoading(true);

        if (!matchType) {
          throw new Error('Invalid match data: Unable to determine match type.');
        }

        let data = [];
        if (matchType === 'singles') {
          data = await getSingleMatch(id); // Fetch match details using the match ID
        } else if (matchType === 'doubles') {
          data = await getDoubleMatch(id); // Fetch match details using the match ID
        }

        // Fetch player details based on match type
        const playerIds = [];
        if (matchType === 'singles') {
          playerIds.push(data.player1, data.player2);
        } else if (matchType === 'doubles') {
          playerIds.push(data.team1_player1, data.team1_player2, data.team2_player1, data.team2_player2);
        }

        const playerDetails = {};
        for (const playerId of playerIds) {
          const player = await getPlayer(playerId);
          playerDetails[playerId] = player;
        }
        console.log('Player Details: ', playerDetails);
        setPlayers(playerDetails);
        setMatch({ ...data }); // Add inferred match type to match data
      } catch (err) {
        console.error('Error fetching match details:', err);
        setError('Failed to fetch match details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    const fetchGames = async () => {
      try {
        const data = await getMatchGames(id, matchType);
        setGames(data.results);
      } catch (err) {
        console.error('Error fetching games:', err);
        setError('Failed to fetch games. Please try again later.');
      }
    };

    if (id) {
      fetchMatchDetails();
      fetchGames();
    }
  }, [id, matchType]);

  if (loading) {
    return <div className="text-center text-white mt-20">Loading match details...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 mt-20">{error}</div>;
  }

  if (!match) {
    return <div className="text-center text-white mt-20">Match details are unavailable.</div>;
  }

  // Function to display the winner's name(s)
  const gameWinnerDisplay = (winner) => {
    if (matchType === 'singles') {
      if (winner === 1) {
        return getPlayerFullname(players[match.player1]) || 'No hay ganador';
      } else if (winner === 2) {
        return getPlayerFullname(players[match.player2]) || 'No hay ganador';
      }
    } else if (matchType === 'doubles') {
      if (winner === 1) {
        return `${getPlayerFullname(players[match.team1_player1])} | ${getPlayerFullname(players[match.team1_player2])}` || 'No hay ganador';
      } else if (winner === 2) {
        return `${getPlayerFullname(players[match.team2_player1])} | ${getPlayerFullname(players[match.team2_player2])}` || 'No hay ganador';
      }
    }
    return 'No hay ganador';
  };

  const matchWinnerDisplay = () => {
    if (matchType === 'singles') {
      return getPlayerFullname(players[match.winner]) || 'No hay ganador';
    } else if (matchType === 'doubles') {
      return `${getPlayerFullname(players[match.winner_1]) || ''} | ${getPlayerFullname(players[match.winner_2]) || ''}` || 'No hay ganador';
    }
    return 'No hay ganador';
  }

  return (
    <div className="bg-gradient-to-r from-gray-800 via-gray-900 to-black min-h-screen text-white flex flex-col">
      <main className="container mx-auto px-4 py-8 flex-grow">
        <h2 className="text-center text-4xl font-bold mb-8">Detalles del Partido</h2>

        <Card className="bg-gray-700 rounded-lg shadow-lg p-6 space-y-8">
          <p className="text-center text-xl font-semibold">
            {matchType === 'singles' ? 'Partido Individual' : 'Partido de Dobles'}
          </p>

          {/* Winner Section */}
          <div className="flex flex-col items-center rounded-lg p-4">
            <Badge color="yellow" className="text-lg font-semibold flex items-center space-x-2 px-4 py-2">
              <TrophyIcon className="h-6 w-6 text-yellow-500" />
              <span>Ganador: { match.winner ? matchWinnerDisplay()  : "No hay ganador"}</span>
            </Badge>
          </div>

          {/* Players Section */}
          <div className="flex justify-center items-center space-x-8">
            {matchType === 'singles' ? (
              <>
                <PlayerCard player={players[match.player1]} />
                <div className="text-4xl font-bold text-white">VS</div>
                <PlayerCard player={players[match.player2]} />
              </>
            ) : (
              <>
                <TeamCard players={[players[match.team1_player1], players[match.team1_player2]]} teamName="Equipo 1" />
                <div className="text-4xl font-bold text-white">VS</div>
                <TeamCard players={[players[match.team2_player1], players[match.team2_player2]]} teamName="Equipo 2" />
              </>
            )}
          </div>

          {/* Match Details */}
          <div className="mt-4 text-lg space-y-2">
            <p><strong>Fecha y Hora:</strong> {new Date(match.date).toLocaleString()}</p>
            <p><strong>Temporada:</strong> {match.season || 'N/A'}</p>
          </div>

          {/* Games Section */}
          <div className="mt-8">
            <h3 className="text-2xl font-bold mb-4">Juegos</h3>
            {games?.length > 0 ? (
              <div className="space-y-4">
                {games.map((game, index) => (
                  <div key={index} className="bg-gray-600 rounded-lg p-4">
                    <p><strong>Juego {index + 1}:</strong></p>
                    <p>
                      {matchType === 'singles'
                        ? `${players[match.player1]?.first_name}: ${game.player1_score} - ${players[match.player2]?.first_name}: ${game.player2_score}`
                        : `Equipo 1: ${game.team1_score} - Equipo 2: ${game.team2_score}`}
                    </p>
                    <p><strong>Ganador:</strong> {gameWinnerDisplay(game.winner)}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p>No hay juegos disponibles para este partido</p>
            )}
          </div>
        </Card>
      </main>
    </div>
  );
}

// **Reusable Components**
const PlayerCard = ({ player }) => (
  <div className="flex flex-col items-center">
    <img
      src={player?.photo || '/assets/images/defaultPlayer.png'}
      alt={`${player?.first_name} ${player?.last_name}`}
      className="w-24 h-24 rounded-full object-cover shadow-lg"
    />
    <div className="text-lg font-semibold mt-2">
      {player?.first_name} {player?.last_name}
    </div>
  </div>
);

const TeamCard = ({ players, teamName }) => (
  <div className="flex flex-col items-center">
    <div className="flex space-x-4">
      {players.map((player, index) => (
        <img
          key={index}
          src={player?.photo || '/assets/images/defaultPlayer.png'}
          alt={`${player?.first_name} ${player?.last_name}`}
          className="w-24 h-24 rounded-full object-cover shadow-lg"
        />
      ))}
    </div>
    <div className="text-lg font-semibold mt-2">{teamName}</div>
  </div>
);

export default MatchDetailCard;
