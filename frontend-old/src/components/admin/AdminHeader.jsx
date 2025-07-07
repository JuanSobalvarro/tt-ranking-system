import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from 'flowbite-react';
import 'styles/tailwind.css';


function AdminHeader() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    console.log('Logging out...');
    // Redirect to the login page
    navigate('/login');
  };

  return (
    <header className="bg-gray-800 text-white py-4 px-6 shadow-md">
      <div className="flex justify-between items-center">
        <Link to="/admin" className="text-2xl font-bold">
          Admin Dashboard
        </Link>
        <div className="relative">
          <button onClick={toggleDropdown} className="flex items-center focus:outline-none">
            <span className="mr-2">Administrador</span>
            <img src={'/assets/adminAvatar.svg'} alt="Avatar" className="w-8 h-8 rounded-full" />
          </button>
          {isDropdownOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white text-gray-800 rounded-md shadow-lg py-2">
              <button
                onClick={handleLogout}
                className="block w-full text-left px-4 py-2 hover:bg-gray-200"
              >
                Cerrar Sesión
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default AdminHeader;
