import React, { useState, useEffect } from 'react';
import { getPlayers, getCurrentSeason, getSeasonForDate } from 'services/api.js';
import { isDateInBetween } from 'services/helpers.js';
import { useBackgroundGradient } from 'services/bgGradient.jsx';
import PlayerSelector from 'components/admin/PlayerSelector.jsx';
import MatchDateTimeInput from 'components/admin/MatchDateTimeInput.jsx';
import GamesManager from 'components/admin/GamesManager.jsx';
import 'styles/tailwind.css';
import AdminFooter from 'components/admin/AdminFooter.jsx';
import AdminHeader from 'components/admin/AdminHeader.jsx';
import { Button } from 'flowbite-react';
import AlertModal from 'components/admin/AlertModal.jsx';
import ConfirmationModal from 'components/admin/ConfirmationModal.jsx';

const initializeSelectedPlayers = (matchType, initialSelectedPlayers) => {
  return matchType === 'singles'
    ? { 0: initialSelectedPlayers?.player1 || null, 1: initialSelectedPlayers?.player2 || null }
    : { 0: initialSelectedPlayers?.team1_player1 || null, 1: initialSelectedPlayers?.team1_player2 || null, 2: initialSelectedPlayers?.team2_player1 || null, 3: initialSelectedPlayers?.team2_player2 || null };
};

const MatchForm = ({ matchType, postMatch, postGame, initialSelectedPlayers, initialMatchDateTime, initialGames }) => {
  const [players, setPlayers] = useState([]);
  const [selectedPlayers, setSelectedPlayers] = useState(initializeSelectedPlayers(matchType, initialSelectedPlayers));
  const [matchDateTime, setMatchDateTime] = useState(initialMatchDateTime || '');
  const [season, setSeason] = useState([]);
  const [games, setGames] = useState(initialGames || [{ team1_score: 0, team2_score: 0 }]);
  const [saving, setSaving] = useState(false);
  const [alert, setAlert] = useState({ isOpen: false, message: '', type: 'success' });
  const [isConfirmationModalOpen, setIsConfirmationModalOpen] = useState(false);

  const backgroundGradient = useBackgroundGradient(selectedPlayers, players, matchType);

  const setPlayerAtIndex = (index, player) => {
    setSelectedPlayers((prev) => ({
      ...prev,
      [index]: player || null,
    }));
  };

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const result = await getPlayers(1, 100);
        setPlayers(result.results);
      } catch (error) {
        console.error('Error fetching players:', error);
      }
    };
    const fetchSeason = async () => {
      try {
        const season = await getCurrentSeason();
        setSeason(season);
      } catch (error) {
        console.error('Error fetching current season:', error);
      }
    };

    // fetchSeason();
    fetchPlayers();
  }, []);

  const handleGameScoreChange = (gameIndex, team, change) => {
    setGames((prevGames) =>
      prevGames.map((game, index) =>
        index === gameIndex
          ? {
              ...game,
              [team]: Math.max(0, game[team] + change),
            }
          : game
      )
    );
  };

  const addNewGame = () => setGames([...games, { team1_score: 0, team2_score: 0 }]);
  const removeGame = (gameIndex) => setGames((prevGames) => prevGames.filter((_, index) => index !== gameIndex));

  const handleSave = async () => {
    const playerIds = Object.values(selectedPlayers);
    if (playerIds.some((id) => !id)) {
        setAlert({
            isOpen: true,
            message: 'Please select all players.',
            type: 'error',
        });
        return;
    }

    if (new Set(playerIds).size !== playerIds.length) {
        setAlert({
            isOpen: true,
            message: 'A player cannot be in more than one team.',
            type: 'error',
        });
        return;
    }

    if (!matchDateTime) {
        setAlert({
            isOpen: true,
            message: 'Please select a date and time for the match.',
            type: 'error',
        });
        return;
    }

    // Check if the date has a season assigned
    const season = await getSeasonForDate(matchDateTime);
    console.log("Season: ", season);
    if (!season) {
        setAlert({
            isOpen: true,
            message: 'No season found for the selected date.',
            type: 'error',
        });
        return;
    }

    if (games.length === 0) {
        setAlert({
            isOpen: true,
            message: 'Please add at least one game.',
            type: 'error',
        });
        return;
    }

    setSaving(true);

    let matchId = null;
    let gameIds = [];

    try {
        const matchData = {
            ...(matchType === 'singles'
                ? {
                    player1: selectedPlayers[0],
                    player2: selectedPlayers[1],
                }
                : {
                    team1_player1: selectedPlayers[0],
                    team1_player2: selectedPlayers[1],
                    team2_player1: selectedPlayers[2],
                    team2_player2: selectedPlayers[3],
                }),
            date: matchDateTime,
        };

        // Save match
        const matchResponse = await postMatch(matchData);
        matchId = matchResponse.id;

        // Save games
        for (let i = 0; i < games.length; i++) {
            const gameData = {
                match: matchId,
                ...(matchType === 'singles'
                    ? {
                        player1_score: games[i].team1_score,
                        player2_score: games[i].team2_score,
                    }
                    : {
                        team1_score: games[i].team1_score,
                        team2_score: games[i].team2_score,
                    }),
            };

            const gameResponse = await postGame(gameData);
            gameIds.push(gameResponse.id);
        }

        setAlert({
            isOpen: true,
            message: 'Match saved successfully.',
            type: 'success',
        });

        // Reset form
        setSelectedPlayers(initializeSelectedPlayers(matchType));
        setMatchDateTime('');
        setGames([{ team1_score: 0, team2_score: 0 }]);

    } catch (error) {
        console.error('Error saving match or games:', error);

        // Rollback mechanism
        if (gameIds.length > 0) {
            console.log('Rolling back games...');
            for (let gameId of gameIds) {
                try {
                    await deleteGame(gameId);
                } catch (deleteError) {
                    console.error(`Failed to delete game with ID ${gameId}:`, deleteError);
                }
            }
        }

        if (matchId) {
            console.log('Rolling back match...');
            try {
                await deleteMatch(matchId);
            } catch (deleteError) {
                console.error(`Failed to delete match with ID ${matchId}:`, deleteError);
            }
        }

        setAlert({
            isOpen: true,
            message: 'An error occurred while saving. Changes were rolled back.',
            type: 'error',
        });
    } finally {
        setSaving(false);
    }
};


  return (
    <div>
      <AlertModal
        isOpen={alert.isOpen}
        message={alert.message}
        type={alert.type}
        onClose={() => setAlert({ ...alert, isOpen: false })}
      />

      <ConfirmationModal
        isOpen={isConfirmationModalOpen}
        onClose={() => setIsConfirmationModalOpen(false)}
      />

      <div
        className="min-h-screen flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8"
        style={{ background: backgroundGradient }}
      >
        <h2 className="text-2xl md:text-4xl font-bold mb-4 md:mb-8 text-center">
          {initialSelectedPlayers ? 'Edit' : 'Add'} {matchType === 'singles' ? 'Singles' : 'Doubles'} Match
        </h2>
        <div className="flex flex-row items-center">
          {matchType === 'singles' ? (
            <div className="flex flex-col md:flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-8 mb-8">
              <PlayerSelector
                players={players}
                selectedPlayer={selectedPlayers[0]}
                setSelectedPlayer={(player) => setPlayerAtIndex(0, player)}
                label="Select Player 1"
              />
              <div className="flex flex-row items-center justify-center">
                <h3 className="text-2xl md:text-4xl font-bold">VS</h3>
              </div>
              <PlayerSelector
                players={players}
                selectedPlayer={selectedPlayers[1]}
                setSelectedPlayer={(player) => setPlayerAtIndex(1, player)}
                label="Select Player 2"
              />
            </div>
          ) : (
            <div className="flex flex-row justify-center items-center space-y-4 md:space-y-0 md:space-x-8 mb-8">
              <div>
                <PlayerSelector
                  players={players}
                  selectedPlayer={selectedPlayers[0]}
                  setSelectedPlayer={(player) => setPlayerAtIndex(0, player)}
                  label="Select Player 1 Team 1"
                />
                <PlayerSelector
                  players={players}
                  selectedPlayer={selectedPlayers[1]}
                  setSelectedPlayer={(player) => setPlayerAtIndex(1, player)}
                  label="Select Player 2 Team 1"
                />
              </div>
              <div className="flex flex-col items-center justify-center">
                <h3 className="text-2xl md:text-4xl font-bold">VS</h3>
              </div>
              <div>
                <PlayerSelector
                  players={players}
                  selectedPlayer={selectedPlayers[2]}
                  setSelectedPlayer={(player) => setPlayerAtIndex(2, player)}
                  label="Select Player 1 Team 2"
                />
                <PlayerSelector
                  players={players}
                  selectedPlayer={selectedPlayers[3]}
                  setSelectedPlayer={(player) => setPlayerAtIndex(3, player)}
                  label="Select Player 2 Team 2"
                />
              </div>
            </div>
          )}
        </div>
        <div className="">
          <MatchDateTimeInput
            matchDateTime={matchDateTime}
            setMatchDateTime={setMatchDateTime}
          />
        </div>
        {console.log("Loading games: ", games)}
        <GamesManager
          games={games}
          handleGameScoreChange={handleGameScoreChange}
          addNewGame={addNewGame}
          removeGame={removeGame}
        />

        <div className="flex justify-center mt-8">
          <Button
            disabled={saving}
            onClick={handleSave}
            className="bg-green-500 text-white hover:bg-primary-dark px-6 py-3 rounded-full"
          >
            {saving ? 'Saving...' : 'Save Match'}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default MatchForm;