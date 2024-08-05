import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import GenericButton from '../components/GenericButton';
import DataTable from '../components/DataTable';
const section = {
  display: 'grid',
  placeItems: 'center',
  alignContent: 'center',
  padding: '25px 0',
  minHeight: '50vh'
}

const careerFields = [
  "Per game",
  "Total",
  "Per minute",
  "Per possession",
  "Advanced",
  "Adjusted Shooting",
  "Play by play",
  "Shooting",
  "Career highs",
  "Playoffs",
];


const Player = () => {
  const location = useLocation();
  const { firstName, lastName } = location.state || { firstName: '', lastName: '' };
  const [playerData, setPlayerData] = useState([]);

  const handleOnClick = (e) => {
    fetch(`http://localhost:5000/player?name=${localStorage.getItem('player')}&type=${e}`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(response => {
      const { data, columnsOrder } = response;
      setPlayerData({ data, columnsOrder });
    })
    .catch(error => console.error('Failed to fetch', error));
  };

  return (
    <div style={section}>
      <h1>Player Page</h1>
      <p>First Name: {firstName}</p>
      <p>Last Name: {lastName}</p>
      <div>
        {careerFields.map((e) => {
          return <GenericButton key={e} name={e} onClick={() => handleOnClick(e)} />
        })}
      </div>
      <div>
        <DataTable playerData={playerData} />
      </div>
    </div>
  );
};

export default Player;
