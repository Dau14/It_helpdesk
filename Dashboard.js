import React, { useState, useEffect } from 'react';

function Dashboard({ token }) {
  const [stats, setStats] = useState({});

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/stats/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) throw new Error('Failed to fetch stats');
        const data = await response.json();
        setStats(data);
      } catch (error) {
        alert(error.message);
      }
    };
    fetchStats();
  }, [token]);

  return (
    <div>
      <h2>Performance Dashboard</h2>
      <p>Avg Resolution Time: {stats.avg_resolution_time}</p>
      <ul>
        {Object.entries(stats.tickets_per_technician || {}).map(([tech, count]) => (
          <li key={tech}>Technician {tech}: {count} tickets</li>
        ))}
      </ul>
    </div>
  );
}

export default Dashboard;