import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from 'pages/visitor/Home.jsx';
import PlayerList from "pages/visitor/players/PlayerList.jsx";
import PlayerDetail from "pages/visitor/players/PlayerDetail.jsx";
import MatchList from "pages/visitor/matches/MatchList.jsx";
import SingleMatchDetail from "pages/visitor/matches/SingleMatchDetail.jsx";
import DoubleMatchDetail from "pages/visitor/matches/DoubleMatchDetail.jsx";
import SeasonList from "pages/visitor/seasons/SeasonList.jsx";
import SeasonDetail from "pages/visitor/seasons/SeasonDetail.jsx";

import ProtectedRoute from 'components/ProtectedRoute.jsx';
import AdminHome from 'pages/admin/Home.jsx';
import AdminLogin from 'pages/admin/AdminLogin.jsx';

import AdminPlayerList from 'pages/admin/players/PlayerList.jsx';
import AdminPlayerAdd from 'pages/admin/players/PlayerAdd.jsx';
import AdminPlayerEdit from 'pages/admin/players/PlayerEdit.jsx';

import AdminMatchesList from 'pages/admin/matches/MatchList.jsx';
import SingleMatchAdd from "pages/admin/matches/SingleMatchAdd.jsx";
import SingleMatchEdit from "pages/admin/matches/SingleMatchEdit.jsx";
import DoubleMatchAdd from "pages/admin/matches/DoubleMatchAdd.jsx";


import AdminSeasonList from "pages/admin/seasons/SeasonList.jsx";
import SeasonAdd from "pages/admin/seasons/SeasonAdd.jsx";
import SeasonEdit from "pages/admin/seasons/SeasonEdit.jsx";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Visitor views */}
          <Route path="/" element={<Home />} />
          <Route path="/players" element={<PlayerList />} />
          <Route path="/players/:id" element={<PlayerDetail />} />
          <Route path="/matches" element={<MatchList />} />
          <Route path="/matches/singles/:id" element={<SingleMatchDetail />} />
          <Route path="/matches/doubles/:id" element={<DoubleMatchDetail />} />
          <Route path="/seasons" element={<SeasonList />} />
          <Route path="/seasons/:id" element={<SeasonDetail />} />
          <Route path="/login" element={<AdminLogin />} />
          {/* Admin Views */}
          <Route path="/admin"
            element={
              <ProtectedRoute>
                <AdminHome />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/players"
            element={
              <ProtectedRoute>
                <AdminPlayerList />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/players/add"
            element={
              <ProtectedRoute>
                <AdminPlayerAdd />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/players/edit/:id"
            element={
              <ProtectedRoute>
                <AdminPlayerEdit />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/matches"
            element={
              <ProtectedRoute>
                <AdminMatchesList />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/matches/singles/add"
            element={
              <ProtectedRoute>
                <SingleMatchAdd />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/matches/singles/edit/:id"
            element={
              <ProtectedRoute>
                <SingleMatchEdit />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/matches/doubles/add"
            element={
              <ProtectedRoute>
                <DoubleMatchAdd />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/seasons"
            element={
              <ProtectedRoute>
                <AdminSeasonList />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/seasons/add"
            element={
              <ProtectedRoute>
                <SeasonAdd />
              </ProtectedRoute>
            }
          />
          <Route path="/admin/seasons/edit/:id"
            element={
              <ProtectedRoute>
                <SeasonEdit />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<h1>Not Found</h1>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;