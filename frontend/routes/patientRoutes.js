const express = require('express');
const router = express.Router();

// Interface patient - affichage rassurant pendant les interactions IA
router.get('/', function (req, res, next) {
  // Données mockées pour le développement
  const patientData = {
    name: 'Jean Dupont',
    familyPhoto: '/images/family-placeholder.jpg', // To replace with real photo
    comfortingMessage: 'You are safe at home, surrounded by your loved ones.',
    currentTime: new Date().toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    }),
    currentDate: new Date().toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  };

  res.render('patient/interface', {
    title: 'MEMO - Your Assistant',
    patient: patientData
  });
});

// Route to receive AI responses (called by AI system)
router.post('/ai-response', function (req, res, next) {
  const { question } = req.body;
  
  // Use a fixed patient ID for now (demo mode)
  const patientId = "7a5c5780-8e97-4e90-be2f-11c2545a4640"; 

  console.log('Processing AI request:', question);

  // OPTIMIZATION: Handle specific demo phrases in Node.js for zero latency
  const lowerQ = question.toLowerCase();
  
  if (lowerQ.includes('time')) {
      const now = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
      return res.json({ success: true, response: `It is currently ${now}.` });
  }
  
  if (lowerQ.includes('hello') || lowerQ.includes('hi')) {
      return res.json({ success: true, response: "Hello! I am MEMO, your assistant. How can I help you today?" });
  }
  
  if (lowerQ.includes('where')) {
      // Mock triggering a perceptual memory exercise
      return res.json({ success: true, response: "You are at your house, You are the Barista of the house. Why don't we make a coffee?" });
  }

  // OPTIMIZATION: Next step in the scenario
  if (lowerQ.includes('yes') || lowerQ.includes('okay') || lowerQ.includes('sure') || lowerQ.includes('check') || lowerQ.includes('do it') || lowerQ.includes('coffee')) {
      return res.json({ success: true, response: "Take the blue jar. Smell the beans." });
  }
  
  if (lowerQ.includes('reminder')) {
      return res.json({ success: true, response: "I have noted that down." });
  }

  // Fallback for any other input (Static, no Python)
  // We mock a generic response since we are suppressing the Python fallback
  return res.json({ success: true, response: "I heard you, but I am in demo mode and only respond to specific triggers." });
});

// Route for standby page
router.get('/standby', function (req, res, next) {
  res.render('patient/standby', {
    title: 'MEMO - Standby'
  });
});

// Route for game page
router.get('/game', function (req, res, next) {
  res.render('patient/game', {
    title: 'MEMO - Memory Game'
  });
});

module.exports = router;