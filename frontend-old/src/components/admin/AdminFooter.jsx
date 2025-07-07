import React from 'react';
import { Link } from 'react-router-dom';
import 'styles/tailwind.css';

function AdminFooter() {
  return (
    <footer className="bg-gray-800 text-white py-4">
      <div className="container mx-auto px-4">
        <div className="flex justify-between">
          <div>
            <Link to="/terms" className="text-sm hover:underline">Terms</Link>
            <Link to="/privacy" className="ml-4 text-sm hover:underline">Privacy Policy</Link>
            <Link to="/contact" className="ml-4 text-sm hover:underline">Contact</Link>
          </div>
          <div>
            <span className="text-sm">&copy; 2024 Table Tennis Ranking System</span>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default AdminFooter;