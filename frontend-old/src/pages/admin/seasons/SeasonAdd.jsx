import React from 'react';
import { useNavigate } from 'react-router-dom';
import { postSeason } from 'services/api.js';
import AdminHeader from 'components/admin/AdminHeader.jsx';
import AdminFooter from 'components/admin/AdminFooter.jsx';
import SeasonForm from 'components/admin/SeasonForm.jsx';

function SeasonAdd() {
  const navigate = useNavigate();

  const handleSubmit = async (formData) => {
    try {
      await postSeason(formData);
      navigate('/admin/seasons');
    } catch (error) {
      console.error('Error creating season:', error);
    }
  };

  return (
    <div className="bg-white min-h-screen text-gray-800 flex flex-col">
      <AdminHeader />
      <main className="container mx-auto px-4 py-8 flex-grow">
        <h2 className="text-center text-4xl font-bold mb-8">Crear Nueva Temporada</h2>
        <SeasonForm onSubmit={handleSubmit} submitText="Crear Temporada" />
      </main>
      <AdminFooter />
    </div>
  );
}

export default SeasonAdd;
