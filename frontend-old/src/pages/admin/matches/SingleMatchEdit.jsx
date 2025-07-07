import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getSingleMatch, getMatchGames, putSingleMatch, putSingleGame } from 'services/api.js';
import MatchForm from 'components/admin/MatchForm.jsx';
import 'styles/tailwind.css';
import AdminFooter from 'components/admin/AdminFooter.jsx';
import AdminHeader from 'components/admin/AdminHeader.jsx';

function SingleMatchEdit() {
  const { id } = useParams();
  const [match, setMatch] = useState(null);
  const [matchDateTime, setMatchDateTime] = useState('');
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMatch = async () => {
      try {
        const matchData = await getSingleMatch(id);
        const matchDateTime = new Date(matchData.date).toISOString().slice(0, 16);
        setMatchDateTime(matchDateTime);
        setMatch(matchData);
      } catch (error) {
        console.error('Error fetching match data:', error);
        setError('Error fetching match data.');
      }
    };

    const fetchGames = async () => {
      try {
        console.log("Fetching games for match with id: ", id);
        const gamesData = await getMatchGames(id, 'singles');
        setGames(gamesData.results);
      } catch (error) {
        console.error('Error fetching games data:', error);
        setError('Error fetching games data.');
      }
    };


    fetchMatch();
    fetchGames();
    setLoading(false);
  }, [id]);

  if (loading) {
    return <div className="text-center text-white mt-20">Loading match details...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 mt-20">{error}</div>;
  }

  if (!match) {
    return <div className="text-center text-white mt-20">No match details available.</div>;
  }

  return (
    <div>
      <AdminHeader />
        {console.log("setting initial games: ", games)}
      <MatchForm
        matchType="singles"
        initialSelectedPlayers={{
          player1: match.player1,
          player2: match.player2,
        }}
        initialMatchDateTime={ matchDateTime }
        initialGames={games.map((game) => ({
          team1_score: game.player1_score,
          team2_score: game.player2_score,
        }))}
        postMatch={async (matchData) => {
          const response = await putSingleMatch(id, matchData);
          return response;
        }}
        postGame={async (gameData) => {
          const response = await putSingleGame(gameData.id, gameData);
          return response;
        }}
      />
      <AdminFooter />
    </div>
  );
}

export default SingleMatchEdit;