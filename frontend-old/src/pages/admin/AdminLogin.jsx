import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { adminLogin } from "services/api.js";
import "styles/tailwind.css";
import { Button, Label, TextInput } from "flowbite-react"; // Import correct components from Flowbite

function AdminLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await adminLogin(username, password);
      console.log(response);
      if (response.access) {
        console.log("Access granted");
        navigate("/admin");
      } else {
        setError("Invalid credentials");
      }
    } catch (err) {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6">Inicio de Sesión</h1>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <Label htmlFor="username" value="Usuario" />
            <TextInput
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              shadow
            />
          </div>
          <div className="mb-6">
            <Label htmlFor="password" value="Contraseña" />
            <TextInput
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              shadow
            />
          </div>
          <Button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
            Entrar como Referee
          </Button>
          <Button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
            Entrar como Jugador
          </Button>
        </form>
        <button
          onClick={() => navigate("/")}
          className="w-full bg-gray-500 text-white py-2 rounded-md hover:bg-gray-600 transition duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 flex items-center justify-center mt-4"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlnsXlink="http://www.w3.org/1999/xlink"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M17 9l4-4m0 0l-4-4m4 4H7m4 4l-4 4m0 0l4 4"
            />
          </svg>
          Volver al inicio
        </button>
      </div>
    </div>
  );
}

export default AdminLogin;
