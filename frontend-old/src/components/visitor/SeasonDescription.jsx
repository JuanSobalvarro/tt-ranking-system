import React from "react";
import { Card } from "flowbite-react";
import { CalendarIcon, TrophyIcon, XCircleIcon } from "@heroicons/react/24/outline";

const SeasonDescription = ({ season }) => {
  return (
    <div className="max-w-2xl mx-auto ">
        <div className="items-center">
          <h1 className="text-3xl font-bold text-gray-800 mb-6 items-center gap-2 text-white">
            Temporada Actual
          </h1>
        </div>


      <Card className="p-6 bg-gray-800 shadow-lg border border-gray-200">
        {season ? (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold text-white">{season.name}</h2>

            <p className="text-lg text-gray-200">
              <strong>Inicio:</strong> {new Date(season.start_date).toLocaleDateString()} <br />
              <strong>Fin:</strong> {new Date(season.end_date).toLocaleDateString()}
            </p>

            {season.description && (
              <blockquote className="italic text-gray-100 border-l-4 pl-4 border-blue-500">
                "{season.description}"
              </blockquote>
            )}

            <div className="bg-gray-900 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-200 mb-2 flex items-center gap-2">
                <TrophyIcon className="h-5 w-5 text-yellow-500" />
                Puntos de la Temporada
              </h3>
              <ul className="text-gray-200 space-y-1">
                <li>
                  <strong>🏆 Individual:</strong> +{season.singles_points_for_win} / -{season.singles_points_for_loss}
                </li>
                <li>
                  <strong>🤝 Dobles:</strong> +{season.doubles_points_for_win} / -{season.doubles_points_for_loss}
                </li>
              </ul>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <XCircleIcon className="h-12 w-12 text-red-500 mb-2" />
            <p className="text-xl text-gray-700">No hay una temporada activa.</p>
          </div>
        )}
      </Card>
    </div>
  );
};

export default SeasonDescription;
