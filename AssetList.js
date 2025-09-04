import React, { useState, useEffect } from 'react';

function AssetList({ token }) {
  const [assets, setAssets] = useState([]);

  useEffect(() => {
    const fetchAssets = async () => {
      try {
        const response = await fetch('/assets/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) throw new Error('Failed to fetch assets');
        const data = await response.json();
        setAssets(data);
      } catch (error) {
        alert(error.message);
      }
    };
    fetchAssets();
  }, [token]);

  return (
    <div>
      <h2>Assets</h2>
      <ul>
        {assets.map((asset) => (
          <li key={asset.id}>
            {asset.name} - Location: {asset.location} - Status: {asset.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AssetList;