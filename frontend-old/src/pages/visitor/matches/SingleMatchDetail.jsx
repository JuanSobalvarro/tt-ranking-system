import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getSingleMatch, getPlayer } from 'services/api'; // Assume this API function fetches match details
import Header from 'components/visitor/Header';
import Footer from 'components/visitor/Footer';
import 'styles/tailwind.css';
import MatchDetailCard from "components/visitor/MatchDetailCard.jsx";

function SingleMatchDetail() {
  return (
    <div className="bg-gradient-to-r from-gray-800 via-gray-900 to-black min-h-screen text-white flex flex-col">
      <Header />
      <MatchDetailCard matchType={'singles'} />
      <Footer />
    </div>
  );
}

export default SingleMatchDetail;
