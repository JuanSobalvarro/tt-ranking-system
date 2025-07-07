import React from "react";
import { useNavigate } from "react-router-dom";
import AdminHeader from "components/admin/AdminHeader";
import AdminFooter from "components/admin/AdminFooter";
import PlayerForm from "components/admin/PlayerForm";
import { addPlayer } from "services/api.js";

function PlayerAdd() {
  const navigate = useNavigate();

  const handleSubmit = async (formData) => {
    const data = new FormData();
    for (const key in formData) {
      if (formData[key]) data.append(key, formData[key]);
    }

    try {
      await addPlayer(data);
      navigate("/admin/players");
    } catch (error) {
      console.error("Error adding player:", error);
    }
  };

  return (
    <div>
      <AdminHeader />
      <main className="container mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">Agregar Jugador</h2>
        <PlayerForm
          initialData={{
            first_name: "",
            last_name: "",
            alias: "",
            gender: "",
            date_of_birth: "",
            nationality: "",
            photo: null,
          }}
          handleSubmit={handleSubmit}
        />
      </main>
      <AdminFooter />
    </div>
  );
}

export default PlayerAdd;
