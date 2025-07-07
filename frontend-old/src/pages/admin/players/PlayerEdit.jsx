import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import AdminHeader from "components/admin/AdminHeader";
import AdminFooter from "components/admin/AdminFooter";
import PlayerForm from "components/admin/PlayerForm";
import { getPlayer, updatePlayer } from "services/api.js";

function PlayerEdit() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [initialData, setInitialData] = useState(null);

  useEffect(() => {
    const fetchPlayer = async () => {
      try {
        const player = await getPlayer(id);
        setInitialData({
          first_name: player.first_name,
          last_name: player.last_name,
          alias: player.alias || "",
          gender: player.gender,
          date_of_birth: player.date_of_birth,
          nationality: player.nationality,
          photo: player.photo || null,
        });
      } catch (error) {
        console.error("Error fetching player data:", error);
      }
    };
    fetchPlayer();
  }, [id]);

  const handleSubmit = async (formData) => {
    const data = new FormData();
    for (const key in formData) {
      if (key === "photo" && formData[key] === null) continue;
      data.append(key, formData[key]);
    }

    try {
      await updatePlayer(id, data);
      navigate("/admin/players");
    } catch (error) {
      console.error("Error updating player:", error);
    }
  };

  return (
    <div>
      <AdminHeader />
      <main className="container mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">Editar Jugador</h2>
        {initialData && <PlayerForm initialData={initialData} handleSubmit={handleSubmit} />}
      </main>
      <AdminFooter />
    </div>
  );
}

export default PlayerEdit;
