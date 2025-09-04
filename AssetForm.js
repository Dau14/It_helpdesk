import React, { useState } from 'react';

function AssetForm({ token }) {
  const [name, setName] = useState('');
  const [location, setLocation] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/assets/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ name, location }),
      });
      if (!response.ok) throw new Error('Failed to create asset');
      alert('Asset created!');
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Asset Name" />
      <input value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Location" />
      <button type="submit">Add Asset</button>
    </form>
  );
}

export default AssetForm;