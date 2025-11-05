import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Config
const SENSOR_API_URL = process.env.SENSOR_API_URL || '';
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || '';

// Patient database file path
const PATIENT_DB_PATH = join(__dirname, 'data', 'patient-database.json');

// Helper functions for patient database
function loadPatientDatabase() {
  try {
    if (existsSync(PATIENT_DB_PATH)) {
      const data = readFileSync(PATIENT_DB_PATH, 'utf8');
      return JSON.parse(data);
    }
  } catch (err) {
    console.error('Error loading patient database:', err);
  }
  // Return default structure if file doesn't exist
  return { patients: [] };
}

function savePatientDatabase(data) {
  try {
    // Ensure directory exists
    const dir = dirname(PATIENT_DB_PATH);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
    writeFileSync(PATIENT_DB_PATH, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (err) {
    console.error('Error saving patient database:', err);
    return false;
  }
}

function getPatientById(patientId) {
  const db = loadPatientDatabase();
  return db.patients.find(p => p.id === patientId || p.preferredName?.toLowerCase() === patientId?.toLowerCase());
}

function getDefaultPatient() {
  const db = loadPatientDatabase();
  return db.patients[0] || null;
}

// Initialize Gemini client if key present
let genAI = null;
if (GEMINI_API_KEY) {
  genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
}

// Dementia-specialized system prompt
const SYSTEM_PROMPT = `You are Memo, a warm, calm, and non-judgmental voice assistant designed to help people living with dementia and their caregivers.

IMPORTANT: You MUST respond ONLY in English. Never respond in French or any other language.

Guidelines:
- Always sound friendly, patient, and reassuring. Avoid complex language.
- Keep responses short (1-2 sentences) unless asked for more.
- Offer gentle orientation cues (time of day, what they might be doing) without insisting.
- Give one clear suggestion at a time. Offer to help rather than command.
- Prioritize safety and wellbeing: hydration, medication adherence reminders (non-prescriptive), rest, contacting a caregiver if needed.
- Never mention dementia directly unless the person brings it up; avoid terms that may cause anxiety.
- If user seems confused, acknowledge feelings and offer simple choices.
- Maintain conversation context and remember what was discussed previously in this session.

Context you may receive:
- Location context (e.g., kitchen). If in kitchen, hydration/medication/reminder may be relevant.
- Profile basics: preferred name, routines (e.g., morning pills), caregiver contact label.
- Conversation history for context continuity.

When proactively greeting after a presence detection:
- Start with a warm hello and the person's preferred name if provided.
- Offer one simple, relevant suggestion (e.g., "Would you like a sip of water?"), then pause for a yes/no.
- If you reference medication, use gentle language like "Would you like a reminder to check your pills?"
`;

// Patient database endpoints
app.get('/api/patient/:id?', (req, res) => {
  const patientId = req.params.id || 'default';
  const patient = patientId === 'default' ? getDefaultPatient() : getPatientById(patientId);
  
  if (!patient) {
    return res.status(404).json({ error: 'Patient not found' });
  }
  
  return res.json(patient);
});

app.get('/api/patients', (req, res) => {
  const db = loadPatientDatabase();
  return res.json({ patients: db.patients });
});

app.post('/api/patient/:id', (req, res) => {
  const patientId = req.params.id;
  const db = loadPatientDatabase();
  const patientIndex = db.patients.findIndex(p => p.id === patientId);
  
  if (patientIndex === -1) {
    return res.status(404).json({ error: 'Patient not found' });
  }
  
  // Update patient data (merge with existing)
  db.patients[patientIndex] = { ...db.patients[patientIndex], ...req.body };
  
  if (savePatientDatabase(db)) {
    return res.json({ success: true, patient: db.patients[patientIndex] });
  } else {
    return res.status(500).json({ error: 'Failed to save patient data' });
  }
});

// Proxy sensor API to avoid CORS and to allow simple config
app.get('/api/sensor', async (req, res) => {
  if (!SENSOR_API_URL) {
    return res.status(500).json({ error: 'SENSOR_API_URL is not configured' });
  }
  try {
    const response = await fetch(SENSOR_API_URL, { timeout: 5000 });
    const data = await response.json();
    return res.json(data);
  } catch (err) {
    return res.status(502).json({ error: 'Failed to reach sensor API', details: String(err) });
  }
});

// In-memory conversation history (session-based, simple implementation)
// In production, use proper session management or database
const conversationHistory = new Map();

// Model to use - try these in order: gemini-1.5-pro, gemini-1.5-flash, gemini-pro
const GEMINI_MODEL = process.env.GEMINI_MODEL || 'gemini-1.5-pro';

// Helper function to list available models
async function listAvailableModels() {
  if (!genAI) return [];
  try {
    // Note: The SDK might not have a direct listModels method
    // We'll try common model names instead
    const commonModels = [
      'gemini-1.5-pro',
      'gemini-1.5-flash',
      'gemini-1.5-pro-latest',
      'gemini-1.5-flash-latest',
      'gemini-pro',
      'gemini-pro-latest'
    ];
    return commonModels;
  } catch (e) {
    console.error('Error listing models:', e);
    return [];
  }
}

// Endpoint to test and list available models
app.get('/api/models', async (req, res) => {
  if (!genAI) {
    return res.status(500).json({ error: 'GEMINI_API_KEY is not configured' });
  }
  
  const modelsToTest = await listAvailableModels();
  const results = [];
  
  for (const modelName of modelsToTest) {
    try {
      const model = genAI.getGenerativeModel({ model: modelName });
      // Try a simple test generation - this will actually call the API
      const result = await model.generateContent('Hello');
      const text = result.response?.text?.() || '';
      results.push({ model: modelName, status: 'available', test: text.substring(0, 50) });
      // Don't break - test all to see what's available
    } catch (e) {
      const errorMsg = e.message || String(e);
      results.push({ 
        model: modelName, 
        status: 'unavailable', 
        error: errorMsg.substring(0, 200) // Limit error message length
      });
    }
  }
  
  // Find first working model
  const workingModel = results.find(r => r.status === 'available');
  
  return res.json({ 
    availableModels: results,
    recommendedModel: workingModel?.model || 'none found',
    suggestion: workingModel 
      ? `Use model: ${workingModel.model}` 
      : 'No models available. Check your API key and region access.'
  });
});

// Generate a proactive assistant message using Gemini
app.post('/api/assistant/respond', async (req, res) => {
  console.log('Received request:', { hasContext: !!req.body?.context, hasUserMessage: !!req.body?.userMessage, sessionId: req.body?.sessionId });
  
  if (!genAI) {
    console.error('GEMINI_API_KEY is not configured');
    return res.status(500).json({ error: 'GEMINI_API_KEY is not configured' });
  }
  const { context, userMessage, sessionId, patientId } = req.body || {};
  const session = sessionId || 'default';
  
  // Load patient data from database
  const patient = patientId ? getPatientById(patientId) : getDefaultPatient();
  const preferredName = context?.preferredName || patient?.preferredName || 'there';
  const location = context?.location || patient?.location || 'home';
  const timeOfDay = context?.timeOfDay || '';
  const familyInfo = patient?.family || {};
  
  console.log('Processing with:', { preferredName, location, timeOfDay, session, hasUserMessage: !!userMessage, patientId });

  try {
    // Try multiple models in order until one works
    const modelsToTry = [
      GEMINI_MODEL,
      'gemini-1.5-pro',
      'gemini-1.5-flash',
      'gemini-1.5-pro-latest',
      'gemini-1.5-flash-latest',
      'gemini-pro',
      'gemini-pro-latest'
    ];
    
    // Cache the working model to avoid testing every time
    if (!global.workingGeminiModel) {
      let model = null;
      let modelName = null;
      let lastError = null;
      
      for (const modelToTry of modelsToTry) {
        try {
          const testModel = genAI.getGenerativeModel({ model: modelToTry });
          // Actually test it with a simple call
          const testResult = await testModel.generateContent('test');
          testResult.response?.text?.(); // Trigger the actual API call
          model = testModel;
          modelName = modelToTry;
          global.workingGeminiModel = { model, name: modelName };
          console.log('✓ Found working Gemini model:', modelName);
          break; // Success, use this model
        } catch (e) {
          console.log(`✗ Model ${modelToTry} not available:`, e.message?.substring(0, 100));
          lastError = e;
          continue;
        }
      }
      
      if (!model) {
        throw new Error(`No available Gemini models found. Tried: ${modelsToTry.join(', ')}. Last error: ${lastError?.message}`);
      }
    }
    
    const { model, name: modelName } = global.workingGeminiModel;
    console.log('Using cached Gemini model:', modelName);
    
    // Get or initialize conversation history for this session
    if (!conversationHistory.has(session)) {
      conversationHistory.set(session, []);
    }
    const history = conversationHistory.get(session);

    // Build conversation context
    let userPrompt;
    if (userMessage && userMessage.trim()) {
      // Conversational mode: user has spoken
      // Add user message to history
      history.push({ role: 'user', text: userMessage.trim() });
      
      // Build conversation context
      let conversationContext = '';
      if (history.length > 1) {
        // Include last few exchanges for context
        const recentHistory = history.slice(-6); // Last 3 exchanges (user + assistant pairs)
        conversationContext = '\nRecent conversation:\n';
        recentHistory.forEach(msg => {
          conversationContext += `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.text}\n`;
        });
      }
      
      // Include family information in context if available
      let familyContext = '';
      if (familyInfo && Object.keys(familyInfo).length > 0) {
        familyContext = `\nFamily information: ${familyInfo.spouse ? `Spouse: ${familyInfo.spouse}` : ''}${familyInfo.children ? `, Children: ${familyInfo.children.join(', ')}` : ''}${familyInfo.caregiver ? `, Caregiver: ${familyInfo.caregiver}` : ''}`;
      }
      
      userPrompt = `Context: location=${location}, timeOfDay=${timeOfDay}, preferredName=${preferredName}${familyContext}${conversationContext}\n` +
        `User just said: "${userMessage.trim()}"\n` +
        'Please respond naturally and helpfully in English, keeping it short (1-2 sentences). Maintain conversation flow and context. You can mention family members if relevant.';
    } else {
      // Proactive mode: no user input, just greeting
      userPrompt = `Context: location=${location}, timeOfDay=${timeOfDay}, preferredName=${preferredName}\n` +
        'Please produce a single short proactive greeting in English and offer of help suitable for speaking aloud.';
    }

    // Build messages for Gemini (using proper format)
    const parts = [];
    
    // Add system prompt as first message
    parts.push(SYSTEM_PROMPT);
    
    // Add conversation history
    history.slice(-10).forEach(msg => {
      parts.push(`\n${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.text}`);
    });
    
    // Add current prompt
    parts.push(`\n${userPrompt}`);

    const fullPrompt = parts.join('\n');
    console.log('Sending to Gemini, prompt length:', fullPrompt.length);
    
    const result = await model.generateContent(fullPrompt);
    
    let text = '';
    try {
      text = result.response?.text?.() || '';
      if (!text && result.response?.candidates?.[0]?.content?.parts?.[0]?.text) {
        text = result.response.candidates[0].content.parts[0].text;
      }
    } catch (e) {
      console.error('Error extracting text from Gemini response:', e);
      console.error('Full response:', JSON.stringify(result.response, null, 2));
    }
    
    if (!text) {
      text = 'Hello, how can I help you today?';
      console.warn('Using fallback text');
    }
    
    console.log('Gemini response:', text);
    
    // Add assistant response to history
    history.push({ role: 'assistant', text });
    
    // Limit history size (keep last 20 messages)
    if (history.length > 20) {
      conversationHistory.set(session, history.slice(-20));
    }
    
    return res.json({ text });
  } catch (err) {
    console.error('Gemini request failed:', err);
    return res.status(500).json({ error: 'Gemini request failed', details: String(err) });
  }
});

app.listen(port, () => {
  console.log(`Memo MVP server running on http://localhost:${port}`);
});



