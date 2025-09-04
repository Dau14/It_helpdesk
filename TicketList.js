import React, { useState, useEffect } from 'react';

function TicketList({ token, role }) {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const response = await fetch('/tickets/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) throw new Error('Failed to fetch tickets');
        const data = await response.json();
        setTickets(data);
      } catch (error) {
        alert(error.message);
      }
    };
    fetchTickets();
  }, [token]);

  return (
    <div>
      <h2>Your Tickets</h2>
      <ul>
        {tickets.map((ticket) => (
          <li key={ticket.id}>
            {ticket.description} - Status: {ticket.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TicketList;