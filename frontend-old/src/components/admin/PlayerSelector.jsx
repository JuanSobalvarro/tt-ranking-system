import React, { useEffect, useState, useRef } from 'react';
import ColorThief from 'colorthief';

const PlayerSelector = ({ players, selectedPlayer, setSelectedPlayer, label }) => {
  const [gradient, setGradient] = useState('bg-white');
  const imgRef = useRef();

  const getPlayerPhoto = (playerId) => {
    const player = players.find((p) => p.id === Number(playerId));
    return player?.photo || '/assets/images/defaultPlayer.png';
  };


  return (
    <div
      className="flex flex-col items-center p-4 rounded"
      style={{ background: gradient }}
    >
      <select
        className="bg-white text-gray-700 px-4 py-2 rounded mb-4 shadow-md"
        value={selectedPlayer || ''}
        onChange={(e) => setSelectedPlayer(e.target.value)}
      >
        <option value="" disabled>
          {label}
        </option>
        {players.map((player) => (
          <option key={player.id} value={player.id}>
            {player.first_name} {player.last_name}
          </option>
        ))}
      </select>
      {selectedPlayer && (
        <img
          ref={imgRef}
          src={getPlayerPhoto(selectedPlayer)}
          alt={label}
          className="w-24 h-24 rounded-full border shadow-md"
        />
      )}
    </div>
  );
};

export default PlayerSelector;
