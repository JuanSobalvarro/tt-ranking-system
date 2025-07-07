import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Button } from "flowbite-react";
import {
  Bars3Icon,
  XMarkIcon,
  HomeIcon,
  UserIcon,
  UserGroupIcon,
  CalendarIcon,
  ClipboardDocumentListIcon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/react/24/outline";

function Header() {
  const location = useLocation(); // Get current route
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Sidebar state
  const [opacity, setOpacity] = useState(1); // Opacity state for scroll effect

  const toggleSidebar = () => setIsSidebarOpen((prev) => !prev);

  useEffect(() => {
    const handleScroll = () => {
      setOpacity(window.scrollY > 50 ? 0.9 : 1); // Adjust opacity on scroll
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div>
      {/* Header */}
      {!isSidebarOpen && (
        <header
          className={`sticky w-full top-0 z-50 bg-gray-900 shadow-md transition-opacity duration-300`}
          style={{ opacity }}
        >
          <div className="container mx-auto flex items-center justify-between px-4 sm:px-6 lg:px-10 py-3 sm:py-4">
            {/* Logo */}
            <Link to="/" className="flex items-center text-white space-x-3">
              <img
                src="/assets/images/clublogo.png"
                alt="Logo"
                className="h-10 sm:h-12"
              />
              <span className="text-lg sm:text-2xl font-semibold">
                Clasificación de Tenis de Mesa
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden sm:flex items-center space-x-6 lg:space-x-8 text-sm sm:text-base text-white font-medium">
              <NavItem to="/" icon={HomeIcon} label="Inicio" active={location.pathname === "/"} />
              <NavItem to="/players/" icon={UserGroupIcon} label="Jugadores" active={location.pathname === "/players/"} />
              <NavItem to="/matches/" icon={ClipboardDocumentListIcon} label="Partidos" active={location.pathname === "/matches/"} />
              <NavItem to="/seasons/" icon={CalendarIcon} label="Temporadas" active={location.pathname === "/seasons/"} />

              <Link
                to="/login/"
                className="flex items-center gap-2 text-green-700 bg-white border-2 border-white rounded-md py-2 px-4 hover:bg-green-700 hover:text-white transition-all"
              >
                <ArrowRightOnRectangleIcon className="w-5 h-5" />
                Iniciar Sesión
              </Link>
            </nav>

            {/* Hamburger Icon (Mobile) */}
            <Button className="text-white sm:hidden bg-gray-900" onClick={toggleSidebar} aria-label="Toggle menu">
              <Bars3Icon className="h-7 w-7" />
            </Button>
          </div>
        </header>
      )}

      {/* Sidebar (Mobile) */}
      <aside
        className={`fixed top-0 left-0 h-full w-64 bg-gray-800 transform ${
          isSidebarOpen ? "translate-x-0" : "-translate-x-full"
        } transition-transform duration-300 shadow-lg z-40`}
      >
        <div className="flex items-center justify-between px-4 py-4">
          <span className="text-white text-lg font-semibold">Menú</span>
          <Button className="text-white bg-gray-800" onClick={toggleSidebar} aria-label="Close menu">
            <XMarkIcon className="h-7 w-7" />
          </Button>
        </div>

        <nav>
          <ul className="flex flex-col space-y-6 px-4 text-white font-medium text-sm">
            <SidebarItem to="/" icon={HomeIcon} label="Inicio" active={location.pathname === "/"} onClick={toggleSidebar} />
            <SidebarItem to="/players/" icon={UserGroupIcon} label="Jugadores" active={location.pathname === "/players/"} onClick={toggleSidebar} />
            <SidebarItem to="/matches/" icon={ClipboardDocumentListIcon} label="Partidos" active={location.pathname === "/matches/"} onClick={toggleSidebar} />
            <SidebarItem to="/seasons/" icon={CalendarIcon} label="Temporadas" active={location.pathname === "/seasons/"} onClick={toggleSidebar} />
            <SidebarItem to="/login/" icon={ArrowRightOnRectangleIcon} label="Iniciar Sesión" onClick={toggleSidebar} />
          </ul>
        </nav>
      </aside>

      {/* Overlay for Sidebar */}
      {isSidebarOpen && (
        <div className="fixed inset-0 bg-black opacity-50 z-30" onClick={toggleSidebar}></div>
      )}
    </div>
  );
}

/** NavItem for Desktop Navigation */
const NavItem = ({ to, icon: Icon, label, active }) => (
  <Link to={to} className={`flex items-center gap-2 hover:text-gray-300 ${active ? "font-bold text-white" : ""}`}>
    <Icon className="w-5 h-5" />
    {label}
  </Link>
);

/** SidebarItem for Mobile Sidebar */
const SidebarItem = ({ to, icon: Icon, label, active, onClick }) => (
  <li>
    <Link to={to} className={`flex items-center gap-3 hover:text-gray-300 ${active ? "font-bold text-white" : ""}`} onClick={onClick}>
      <Icon className="w-6 h-6" />
      {label}
    </Link>
  </li>
);

export default Header;
