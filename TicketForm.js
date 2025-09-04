import React, { useState } from 'react';

function TicketForm({ token }) {
  const [description, setDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/tickets/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ description }),
      });
      if (!response.ok) throw new Error('Failed to submit ticket');
      alert('Ticket submitted!');
      setDescription('');
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Describe issue" />
      <button type="submit">Submit Ticket</button>
    </form>
  );
}

export default TicketForm;