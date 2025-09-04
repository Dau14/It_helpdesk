import React, { useState } from 'react';

function AdminPanel({ token }) {
  const [ticketId, setTicketId] = useState('');
  const [status, setStatus] = useState('');
  const [assignedTo, setAssignedTo] = useState('');

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`/tickets/${ticketId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ status, assigned_to: assignedTo }),
      });
      if (!response.ok) throw new Error('Failed to update ticket');
      alert('Ticket updated!');
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div>
      <h2>Admin Panel</h2>
      <form onSubmit={handleUpdate}>
        <input type="number" value={ticketId} onChange={(e) => setTicketId(e.target.value)} placeholder="Ticket ID" />
        <input type="text" value={status} onChange={(e) => setStatus(e.target.value)} placeholder="New Status" />
        <input type="number" value={assignedTo} onChange={(e) => setAssignedTo(e.target.value)} placeholder="Assign To User ID" />
        <button type="submit">Update Ticket</button>
      </form>
    </div>
  );
}

export default AdminPanel;