import React from 'react';
import MatchForm from 'components/admin/MatchForm.jsx';
import { postSingleMatch, postSingleGame } from 'services/api.js';
import AdminHeader from "components/admin/AdminHeader.jsx";
import AdminFooter from "components/admin/AdminFooter.jsx";

const SingleMatchAdd = () => (
    <div>
      <AdminHeader />
      <MatchForm
        matchType="singles"
        postMatch={postSingleMatch}
        postGame={postSingleGame}
      />
      <AdminFooter />
    </div>
);

export default SingleMatchAdd;