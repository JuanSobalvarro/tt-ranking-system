import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getSeason, putSeason } from 'services/api.js';
import AdminHeader from 'components/admin/AdminHeader.jsx';
import AdminFooter from 'components/admin/AdminFooter.jsx';
import SeasonForm from 'components/admin/SeasonForm.jsx';

function SeasonEdit() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [seasonData, setSeasonData] = useState(null);

  useEffect(() => {
    async function fetchSeason() {
      try {
        const response = await getSeason(id);
        // console.log('Season data:', response);
        setSeasonData(response);
      } catch (error) {
        console.error('Error fetching season:', error);
      }
    }
    fetchSeason();
  }, [id]);

  const handleSubmit = async (formData) => {
    try {
      await putSeason(id, formData);
      navigate('/admin/seasons');
    } catch (error) {
      console.error('Error updating season:', error);
    }
  };

  return (
    <div className="bg-white min-h-screen text-gray-800 flex flex-col">
      <AdminHeader />
      <main className="container mx-auto px-4 py-8 flex-grow">
        <h2 className="text-center text-4xl font-bold mb-8">Editar Temporada</h2>
        {seasonData ? <SeasonForm initialData={seasonData} onSubmit={handleSubmit} submitText="Actualizar Temporada" /> : <p>Cargando...</p>}
      </main>
      <AdminFooter />
    </div>
  );
}

export default SeasonEdit;
