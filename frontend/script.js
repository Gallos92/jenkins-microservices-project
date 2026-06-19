const API_URL = 'http://api:5000';

fetch(API_URL + '/health')
  .then(res => res.json())
  .then(data => {
    document.getElementById('api-status').innerText = 'API is ' + data.status;
  })
  .catch(() => {
    document.getElementById('api-status').innerText = 'API is unreachable';
  });

fetch(API_URL + '/api/data')
  .then(res => res.json())
  .then(data => {
    document.getElementById('api-data').innerText = JSON.stringify(data, null, 2);
  })
  .catch(() => {
    document.getElementById('api-data').innerText = 'Could not fetch data';
  });
