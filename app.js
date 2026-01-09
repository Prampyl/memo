const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const session = require('express-session');
const crypto = require('crypto'); // Ajout de la bibliothèque crypto
const multer = require('multer'); // Importation de multer pour gérer les fichiers
var cors = require('cors');


//const authRoutes = require('./routes/authRoutes');
const frontendRouter = require('./frontend/index'); // Use frontend router
/* const candidatRoutes = require('./routes/candidatRoutes');
const profileRoutes = require('./routes/profileRoutes');
const recruteurRoutes = require('./routes/recruteurRoutes');
const adminRoutes = require('./routes/adminRoutes');
const demandeRoutes = require('./routes/demandeRoutes'); */

const app = express();

app.use(cors());
// Middleware de base
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
// Update static files to point to frontend/public
app.use(express.static(path.join(__dirname, 'frontend/public')));

// Génération d'une clé secrète sécurisée
const sessionSecret = crypto.randomBytes(32).toString('hex');

// Configuration des sessions
app.use(session({
  secret: sessionSecret, // Utilisation de la clé générée
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: false,
    maxAge: 24 * 60 * 60 * 1000 // 24 heures
  }
}));

// Middleware pour gérer les promesses
app.use((req, res, next) => {
  Promise.resolve()
    .then(() => next())
    .catch(err => next(err));
});

// Configuration des vues
// Point to frontend directory for views
app.set('views', path.join(__dirname, 'frontend'));
app.set('view engine', 'ejs');

// Routes publiques
app.use('/', frontendRouter);
//app.use('/auth', authRoutes);

// Routes protégées avec leurs middlewares spécifiques
/* app.use('/candidat', candidatRoutes);
app.use('/profile', profileRoutes);
app.use('/recruteur', recruteurRoutes);
app.use('/admin', adminRoutes);
app.use('/demandes', demandeRoutes); */
/*
// Route API pour retourner les offres publiées (sans auth) Test pour Vue.js
app.get('/api/offres', async (req, res) => {
  try {
    const { getPublishedOffres } = require('./models/candidatModel');
    const offres = await getPublishedOffres();
    res.json(offres);
  } catch (err) {
    res.status(500).json({ error: 'Erreur lors de la récupération des offres.' });
  }
});
*/

// 404 Error handling
app.use((req, res, next) => {
  res.status(404).render('error', { message: 'Page not found' });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).render('error', {
    message: err.message || 'Server Error',
    error: process.env.NODE_ENV === 'development' ? err : {}
  });
});

// Démarrage du serveur si ce fichier est exécuté directement
if (require.main === module) {
  const port = process.env.PORT || 3000;
  app.listen(port, () => {
    console.log(`Serveur démarré sur le port ${port}`);
  });
}

module.exports = app;