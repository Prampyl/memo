var express = require('express');
var router = express.Router();

/* Page d'accueil */
router.get('/', function (req, res, next) {
  res.render('home');
});

// Demo Presentation Route
router.get('/demo', function (req, res, next) {
  res.render('demo', { title: 'MEMO Presentation' });
});

// Importation des routes caregiver
const caregiverRoutes = require('./routes/caregiverRoutes');
router.use('/caregiver', caregiverRoutes);

// Importation des routes patient
const patientRoutes = require('./routes/patientRoutes');
router.use('/patient', patientRoutes);

module.exports = router;