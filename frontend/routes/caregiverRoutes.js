const express = require('express');
const router = express.Router();

// Simulate data for development (replace with real DB calls)
const mockPatient = {
  id: 1,
  name: 'John Doe',
  age: 72,
  diagnosis: 'Mild Alzheimer\'s',
  medications: ['Donepezil 10mg', 'Vitamin D'],
  lastCheckup: '2024-01-15',
  emergencyContact: '+33123456789'
};

const mockInteractions = [
  {
    id: 1,
    date: '2024-01-05 10:30',
    question: 'What time is it?',
    answer: 'It is 10:30 AM.',
    type: 'temporal'
  },
  {
    id: 2,
    date: '2024-01-05 14:15',
    question: 'Where am I?',
    answer: 'You are at home, in your living room.',
    type: 'spatial'
  },
  {
    id: 3,
    date: '2024-01-04 16:45',
    question: 'Who am I?',
    answer: 'You are John Doe, you are 72 years old.',
    type: 'identity'
  }
];

// Main caregiver route
router.get('/', function (req, res, next) {
  res.render('caregiver/dashboard', {
    title: 'Caregiver Dashboard',
    patient: mockPatient,
    interactions: mockInteractions
  });
});

// Route to view patient details
router.get('/patient/:id', function (req, res, next) {
  // Here, retrieve patient data from DB
  res.render('caregiver/patient', {
    title: 'Patient Information',
    patient: mockPatient
  });
});

// Route to add/update patient information
router.post('/patient/:id/update', function (req, res, next) {
  // Here, update data in DB
  console.log('Patient update:', req.body);
  res.redirect('/caregiver');
});

// Route to view AI interactions
router.get('/interactions', function (req, res, next) {
  res.render('caregiver/interactions', {
    title: 'AI Interactions',
    interactions: mockInteractions
  });
});

module.exports = router;