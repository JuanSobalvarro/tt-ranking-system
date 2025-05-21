import React, { useEffect, useState } from 'react';
import { Link } from "react-router-dom";
import AdminHeader from 'components/admin/AdminHeader';
import AdminFooter from 'components/admin/AdminFooter';
import { getAdminHomeData } from 'services/api.js';
import 'styles/tailwind.css';

function AdminHome() {
  const [data, setData] = useState({
    registered_players: 0,
    single_matches_played_last_3days: 0,
    double_matches_played_last_3days: 0,
    most_active_players_last_week: [],
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getAdminHomeData();
        setData(result);
      } catch (error) {
        console.error('Error fetching admin home data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="bg-gray-100 min-h-screen">
      <AdminHeader />
      <main className="container mx-auto px-4 py-8">
        {/* Admin Dashboard Title */}
        <h1 className="text-4xl font-bold mb-6 text-gray-800">Admin Dashboard</h1>

        {/* Quick Access Section */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">Quick Access</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-blue-500 text-white rounded-lg shadow-lg p-6">
              <h3 className="font-semibold text-lg mb-2">Manage Players</h3>
              <p className="text-sm mb-4">View, add, and edit player details.</p>
              <Link
                to="/admin/players"
                className="inline-block px-4 py-2 bg-white text-blue-500 rounded hover:bg-blue-100 transition">
                View Players
              </Link>
            </div>
            <div className="bg-green-500 text-white rounded-lg shadow-lg p-6">
              <h3 className="font-semibold text-lg mb-2">Manage Matches</h3>
              <p className="text-sm mb-4">Schedule and track match details.</p>
              <Link
                to="/admin/matches"
                className="inline-block px-4 py-2 bg-white text-green-500 rounded hover:bg-green-100 transition">
                View Matches
              </Link>
            </div>
            <div className="bg-yellow-500 text-white rounded-lg shadow-lg p-6">
              <h3 className="font-semibold text-lg mb-2">Manage Seasons</h3>
              <p className="text-sm mb-4">Manage system seasons.</p>
              <Link
                to="/admin/seasons"
                className="inline-block px-4 py-2 bg-white text-yellow-500 rounded hover:bg-yellow-100 transition">
                View Seasons
              </Link>
            </div>
          </div>
        </section>

        {/* Data Overview Section */}
        <section className="mb-8">
          <div className="bg-white shadow-md rounded-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Registered Players</h2>
            <p className="text-5xl font-bold text-blue-600">{data.registered_players}</p>
          </div>
        </section>

        {/* Matches Played in Last 3 Days */}
        <section className="mb-8">
          <div className="bg-white shadow-md rounded-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Matches Played in the Last 3 Days</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-800">Singles</h3>
                <p className="text-3xl text-blue-500">{data?.single_matches_played_last_3days}</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-800">Doubles</h3>
                <p className="text-3xl text-green-500">{data?.double_matches_played_last_3days}</p>
              </div>
            </div>
          </div>
        </section>

        {/* Most Active Players Section */}
        <section className="mb-8">
          <div className="bg-white shadow-md rounded-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Most Active Players Last Week</h2>
            <ul className="space-y-3">
              {Array.isArray(data?.most_active_players_last_week) && data.most_active_players_last_week.length > 0 ? (
                data.most_active_players_last_week.map((player, index) => (
                  <li
                    key={player.player_id || index}
                    className="bg-gray-50 rounded p-4 shadow-sm hover:bg-gray-100 transition">
                    <div className="flex justify-between">
                      <span className="font-medium text-gray-800">Player: {player.player_name}</span>
                      <span className="font-bold text-blue-500">{player.matches_played_last_week} Matches</span>
                    </div>
                  </li>
                ))
              ) : (
                <p className="text-gray-500">No active players in the last week.</p>
              )}
            </ul>
          </div>
        </section>

      </main>
      <AdminFooter />
    </div>
  );
}

export default AdminHome;
