import React, { useState, useEffect } from 'react';
import { getSeason } from 'services/api.js';
import { Card, Badge } from 'flowbite-react';

function RankingCardDetail({ ranking }) {
    const [season, setSeason] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSeason = async () => {
            try {
                const response = await getSeason(ranking.season);
                setSeason(response);
            } catch (error) {
                console.error('Error fetching season:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchSeason();
    }, [ranking.season]);

    return (
        <Card className="max-w-xl bg-gray-900 border border-gray-700 shadow-xl">
            <h3 className="text-2xl font-extrabold text-green-400 mb-2">
                {loading ? 'Cargando...' : season?.name || 'Desconocida'}
            </h3>

            <div className="flex justify-between text-sm text-gray-400">
                <p>📅 Inicio: {season?.start_date || 'N/A'}</p>
                <p>📅 Fin: {season?.end_date || 'N/A'}</p>
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
                <Badge color="purple">Ranking: {ranking.ranking}</Badge>
                <Badge color="blue">Partidos: {ranking.matches_played}</Badge>
                <Badge color="green">Victorias Ind.: {ranking.singles_victories}</Badge>
                <Badge color="yellow">Victorias Dobles: {ranking.doubles_victories}</Badge>
            </div>
        </Card>
    );
}

export default RankingCardDetail;
