import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getDoubleMatch, getPlayer } from 'services/api';
import Header from 'components/visitor/Header';
import Footer from 'components/visitor/Footer';
import 'styles/tailwind.css';
import MatchDetailCard from "components/visitor/MatchDetailCard.jsx";

function DoubleMatchDetail() {
  const { id } = useParams();
  const [match, setMatch] = useState(null);
  const [team1Player1, setTeam1Player1] = useState(null);
  const [team1Player2, setTeam1Player2] = useState(null);
  const [team2Player1, setTeam2Player1] = useState(null);
  const [team2Player2, setTeam2Player2] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMatchDetails = async () => {
      try {
        setLoading(true);
        const data = await getDoubleMatch(id);
        const team1p1 = await getPlayer(data.team1_player1);
        const team1p2 = await getPlayer(data.team1_player2);
        const team2p1 = await getPlayer(data.team2_player1);
        const team2p2 = await getPlayer(data.team2_player2);

        setTeam1Player1(team1p1);
        setTeam1Player2(team1p2);
        setTeam2Player1(team2p1);
        setTeam2Player2(team2p2);
        setMatch(data);
      } catch (err) {
        console.error('Error fetching match details:', err);
        setError('Failed to fetch match details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchMatchDetails();
  }, [id]);

  if (loading) {
    return <div className="text-center text-white mt-20">Loading match details...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500 mt-20">{error}</div>;
  }

  return (
      <div className="bg-gradient-to-r from-gray-800 via-gray-900 to-black min-h-screen text-white flex flex-col">
        <Header/>
        <MatchDetailCard matchType={'doubles'}/>
        <Footer/>
      </div>
  );
}

export default DoubleMatchDetail;
