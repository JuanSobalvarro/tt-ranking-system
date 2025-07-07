import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub, faTwitter } from "@fortawesome/free-brands-svg-icons";

import "styles/tailwind.css";

function Footer() {
  return (
    <footer className="bg-gray-900 text-white py-8">
      <div className="container mx-auto px-6 sm:px-8">
        {/* Footer Content Section */}
        <div className="flex flex-wrap justify-between sm:justify-evenly text-sm mb-6">
          {/* Developed By Section */}
          <div className="w-full sm:w-auto text-center sm:text-left mb-4 sm:mb-0">
            <h6 className="font-bold uppercase mb-2">Desarrollado por Juan Sobalvarro</h6>
            <p className="text-gray-400">Sistema de Clasificación de Tenis de Mesa</p>
          </div>

          {/* Contact Section */}
          <div className="w-full sm:w-auto text-center sm:text-left mb-4 sm:mb-0">
            <h6 className="font-bold uppercase mb-2">Contacto</h6>
            <p className="text-gray-400">
              Email:{" "}
              <Link
                to="mailto:sobalvarrog.juans@gmail.com"
                className="underline text-blue-400 hover:text-blue-500"
              >
                sobalvarrog.juans@gmail.com
              </Link>
            </p>
            <p className="text-gray-400">
              Email:{" "}
              <Link
                to="mailto:juan.sobalvarro@est.ulsa.edu.ni"
                className="underline text-blue-400 hover:text-blue-500"
              >
                juan.sobalvarro@est.ulsa.edu.ni
              </Link>
            </p>
          </div>

          {/* Social Media Section */}
          <div className="w-full sm:w-auto text-center sm:text-left">
            <h6 className="font-bold uppercase mb-2">Sígueme</h6>
            <div className="flex justify-center sm:justify-start space-x-4">
              <Link
                to="https://github.com/JuanSobalvarro"
                target="_blank"
                className="text-xl text-gray-400 hover:text-white"
                aria-label="Github"
              >
                <FontAwesomeIcon icon={faGithub} />
              </Link>
              <Link
                to="https://x.com/JuanSobalvarroG"
                target="_blank"
                className="text-xl text-gray-400 hover:text-white"
                aria-label="Twitter"
              >
                <FontAwesomeIcon icon={faTwitter} />
              </Link>
            </div>
          </div>
        </div>

        {/* Footer Bottom Section */}
        <div className="text-center py-2 border-t border-gray-700 mt-6">
          <Link
            to="https://github.com/JuanSobalvarro/tt-ranking-system"
            className="text-gray-400 text-sm hover:text-white"
            aria-label="GitHub Repository"
          >
            © 2024 Sistema de Clasificación de Tenis de Mesa v2.1.0
          </Link>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
