import React from 'react';

const GamesManager = ({ games, handleGameScoreChange, addNewGame, removeGame }) => (
  <div className="w-full max-w-2xl z-10">
    {games.map((game, index) => (
      <div
        key={index}
        className="flex justify-between items-center mb-4 bg-white shadow-md px-4 py-2 rounded"
      >
        <div className="flex items-center space-x-4">
          <button
            onClick={() => handleGameScoreChange(index, 'team1_score', -1)}
            className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
          >
            -
          </button>
          <span>{game.team1_score}</span>
          <button
            onClick={() => handleGameScoreChange(index, 'team1_score', 1)}
            className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
          >
            +
          </button>
        </div>
        <span>Juego {index + 1}</span>
        <div className="flex items-center space-x-4">
          <button
            onClick={() => handleGameScoreChange(index, 'team2_score', -1)}
            className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
          >
            -
          </button>
            {/*{console.log(game)}*/}
          <span>{game.team2_score}</span>
          <button
            onClick={() => handleGameScoreChange(index, 'team2_score', 1)}
            className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
          >
            +
          </button>
        </div>
        <button
          onClick={() => removeGame(index)}
          className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
        >
          Eliminar
        </button>
      </div>
    ))}
    <button
      onClick={addNewGame}
      className="bg-blue-500 text-white px-4 py-2 rounded mt-4 hover:bg-blue-600"
    >
      Agregar Juego
    </button>
  </div>
);

export default GamesManager;
