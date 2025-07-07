import React, { useEffect, useState } from 'react';
import { getSeasons, deleteSeason } from 'services/api.js';
import AdminHeader from 'components/admin/AdminHeader';
import AdminFooter from 'components/admin/AdminFooter';
import { Spinner, Button, Table } from 'flowbite-react';
import { Link } from 'react-router-dom';
import ConfirmationModal from 'components/admin/ConfirmationModal';
import 'styles/tailwind.css';

function AdminSeasonList() {
  const [seasons, setSeasons] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [seasonToDelete, setSeasonToDelete] = useState(null);

  const seasonsPerPage = 10;

  const fetchSeasons = async () => {
    try {
      const result = await getSeasons(currentPage, seasonsPerPage);
      setSeasons(result.results);
      setTotalPages(Math.ceil(result.count / seasonsPerPage));
    } catch (error) {
      console.error('Error fetching seasons:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = (seasonId) => {
    setSeasonToDelete(seasonId);
    setIsModalOpen(true);
  };

  const confirmDelete = async () => {
    if (seasonToDelete) {
      try {
        await deleteSeason(seasonToDelete);
        fetchSeasons(); // Refresh the list
      } catch (error) {
        console.error('Error deleting season:', error);
      } finally {
        setIsModalOpen(false);
        setSeasonToDelete(null);
      }
    }
  };

  useEffect(() => {
    setLoading(true);
    fetchSeasons();
  }, [currentPage]);

  return (
    <div className="bg-white min-h-screen text-gray-800 flex flex-col">
      <AdminHeader />
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-grow">
        <div className="flex flex-col md:flex-row justify-between items-center mb-6 space-y-4 md:space-y-0">
          <h2 className="text-2xl md:text-4xl font-bold text-center md:text-left">
            Lista de Temporadas
          </h2>
          <Link to="/admin/seasons/add">
            <Button className="bg-blue-600 hover:bg-blue-700 w-full md:w-auto">
              Crear Temporada
            </Button>
          </Link>
        </div>
        {loading ? (
          <div className="flex justify-center items-center">
            <Spinner size="xl" />
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <Table striped>
                <Table.Head>
                  <Table.HeadCell>ID</Table.HeadCell>
                  <Table.HeadCell>Nombre</Table.HeadCell>
                  <Table.HeadCell>Fecha de Inicio</Table.HeadCell>
                  <Table.HeadCell>Fecha de Fin</Table.HeadCell>
                  <Table.HeadCell>Acciones</Table.HeadCell>
                </Table.Head>
                <Table.Body>
                  {seasons.length > 0 ? (
                    seasons.map((season) => (
                      <Table.Row key={season.id}>
                        <Table.Cell>{season.id}</Table.Cell>
                        <Table.Cell>{season.name}</Table.Cell>
                        <Table.Cell>{new Date(season.start_date).toLocaleDateString()}</Table.Cell>
                        <Table.Cell>{new Date(season.end_date).toLocaleDateString()}</Table.Cell>
                        <Table.Cell>
                          <div className="flex justify-center space-x-2">
                            <Link
                              to={`/admin/seasons/edit/${season.id}`}
                              className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                            >
                              Editar
                            </Link>
                            <Button
                              onClick={() => handleDelete(season.id)}
                              className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                            >
                              Eliminar
                            </Button>
                          </div>
                        </Table.Cell>
                      </Table.Row>
                    ))
                  ) : (
                    <Table.Row>
                      <Table.Cell colSpan="5" className="text-center text-gray-500 py-4">
                        No hay temporadas registradas.
                      </Table.Cell>
                    </Table.Row>
                  )}
                </Table.Body>
              </Table>
            </div>
            <div className="flex flex-col md:flex-row justify-between items-center mt-4 space-y-4 md:space-y-0">
              <Button
                onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 w-full md:w-auto"
              >
                Anterior
              </Button>
              <span className="text-gray-600 text-center">{`Página ${currentPage} de ${totalPages}`}</span>
              <Button
                onClick={() => setCurrentPage((prev) => prev + 1)}
                disabled={currentPage === totalPages}
                className="bg-gray-200 text-gray-800 px-4 py-2 rounded hover:bg-gray-300 w-full md:w-auto"
              >
                Siguiente
              </Button>
            </div>
          </>
        )}
      </main>
      <AdminFooter />

      {/* Confirmation Modal */}
      <ConfirmationModal
        isOpen={isModalOpen}
        onConfirm={confirmDelete}
        onCancel={() => setIsModalOpen(false)}
        message="¿Estás seguro de que deseas eliminar esta temporada?"
        deleteItem="Eliminar"
        cancelItem="Cancelar"
      />
    </div>
  );
}

export default AdminSeasonList;
