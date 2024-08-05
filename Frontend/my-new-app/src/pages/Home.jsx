import React, { useState } from 'react';
import { Button, TextField, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const section = {
  display: 'grid',
  placeItems: 'center',
  alignContent: 'center',
  padding: '25px 0',
  height: '50vh'
}

const Home = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:5000/create_player', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ firstName, lastName }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log(data);
      // Navigate to the player page
      localStorage.setItem('player', data.player_name)
      navigate('/player', { state: { firstName, lastName } });
    } catch (error) {
      console.error('Failed to fetch', error);
    }
  };

  return (
    <div style={section}>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ display: 'flex', flexDirection: 'column', gap: 2, width: '300px', margin: 'auto' }}
      >
        <TextField
          label="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          required
        />
        <TextField
          label="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          required
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={!firstName || !lastName}
        >
          Submit
        </Button>
      </Box>
    </div>
  );
};

export default Home;