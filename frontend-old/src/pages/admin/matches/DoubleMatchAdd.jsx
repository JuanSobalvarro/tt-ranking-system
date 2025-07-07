import React from 'react';
import MatchForm from 'components/admin/MatchForm.jsx';
import { postDoubleMatch, postDoubleGame } from 'services/api.js';

const DoubleMatchAdd = () => (
  <MatchForm
    matchType="doubles"
    postMatch={postDoubleMatch}
    postGame={postDoubleGame}
  />
);

export default DoubleMatchAdd;