import React, { useEffect, useState } from "react";
import { getSeasons } from "services/api"; // Fetches the seasons from the backend
import Header from "components/visitor/Header";
import Footer from "components/visitor/Footer";
import { Table, Spinner, Button } from "flowbite-react"; // Flowbite components
import "styles/tailwind.css";
import { Link } from "react-router-dom";

function SeasonList() {
  const [seasons, setSeasons] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSeasons = async () => {
      try {
        const data = await getSeasons(); // Fetch the seasons
        setSeasons(data.results);
      } catch (error) {
        console.error("Error fetching seasons:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSeasons();
  }, []);

  return (
    <div className="bg-gradient-to-r from-gray-800 via-gray-900 to-black min-h-screen text-white flex flex-col">
      <Header />
      <main className="container mx-auto px-4 py-8 flex-grow">
        <h2 className="text-center text-4xl font-bold mb-8">Lista de Temporadas</h2>

        {/* Loading State */}
        {isLoading ? (
          <div className="flex justify-center items-center h-64">
            <Spinner color="success" size="xl" />
          </div>
        ) : (
          <div className="overflow-x-auto">
            <Table hoverable className="w-full">
              <Table.Head>
                <Table.HeadCell className="bg-gray-700 text-white">ID</Table.HeadCell>
                <Table.HeadCell className="bg-gray-700 text-white">Nombre</Table.HeadCell>
                <Table.HeadCell className="bg-gray-700 text-white">Fecha de Inicio</Table.HeadCell>
                <Table.HeadCell className="bg-gray-700 text-white">Fecha de Fin</Table.HeadCell>
                <Table.HeadCell className="bg-gray-700 text-white">Detalles</Table.HeadCell>
              </Table.Head>
              <Table.Body className="divide-y">
                {seasons.length > 0 ? (
                  seasons.map((season) => (
                    <Table.Row key={season.id} className="bg-gray-800 hover:bg-gray-700">
                      <Table.Cell>{season.id}</Table.Cell>
                      <Table.Cell className="font-medium text-emerald-400">{season.name}</Table.Cell>
                      <Table.Cell>{new Date(season.start_date).toLocaleDateString()}</Table.Cell>
                      <Table.Cell>{new Date(season.end_date).toLocaleDateString()}</Table.Cell>
                      <Table.Cell>
                        <Link to={`/seasons/${season.id}`}>
                          <Button size="sm" className="bg-gray-800 text-emerald-400">
                            Ver Detalles
                          </Button>
                        </Link>
                      </Table.Cell>
                    </Table.Row>
                  ))
                ) : (
                  <Table.Row>
                    <Table.Cell colSpan="5" className="text-center text-gray-400 py-4">
                      No hay temporadas disponibles.
                    </Table.Cell>
                  </Table.Row>
                )}
              </Table.Body>
            </Table>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}

export default SeasonList;
