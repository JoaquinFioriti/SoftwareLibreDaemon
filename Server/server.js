const express = require('express');
const app = express();
const PORT = 3000; 


app.get('/', (req, res) => {
  res.send('Server de prueba para el tp daemon');
});

app.listen(PORT, () => {
  console.log(`Servidor Express en funcionamiento en http://localhost:${PORT}`);
});