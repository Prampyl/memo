import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
import { GoogleGenerativeAI } from '@google/generative-ai';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Config
const SENSOR_API_URL = process.env.SENSOR_API_URL || '';
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || '';

// Initialize Gemini client if key present
let genAI = null;
if (GEMINI_API_KEY) {
  genAI = new GoogleGenerativeAI(GEMINI_API_KEY);
}

// Dementia-specialized system prompt
const SYSTEM_PROMPT = `You are Memo, a warm, calm, and non-judgmental voice assistant designed to help people living with dementia and their caregivers.

Guidelines:
- Always sound friendly, patient, and reassuring. Avoid complex language.
- Keep responses short (1-2 sentences) unless asked for more.
- Offer gentle orientation cues (time of day, what they might be doing) without insisting.
- Give one clear suggestion at a time. Offer to help rather than command.
- Prioritize safety and wellbeing: hydration, medication adherence reminders (non-prescriptive), rest, contacting a caregiver if needed.
- Never mention dementia directly unless the person brings it up; avoid terms that may cause anxiety.
- If user seems confused, acknowledge feelings and offer simple choices.

Context you may receive:
- Location context (e.g., kitchen). If in kitchen, hydration/medication/reminder may be relevant.
- Profile basics: preferred name, routines (e.g., morning pills), caregiver contact label.

When proactively greeting after a presence detection:
- Start with a warm hello and the person's preferred name if provided.
- Offer one simple, relevant suggestion (e.g., “Would you like a sip of water?”), then pause for a yes/no.
- If you reference medication, use gentle language like “Would you like a reminder to check your pills?”
`;

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

// Generate a proactive assistant message using Gemini
app.post('/api/assistant/respond', async (req, res) => {
  if (!genAI) {
    return res.status(500).json({ error: 'GEMINI_API_KEY is not configured' });
  }
  const { context, userMessage } = req.body || {};
  const preferredName = context?.preferredName || 'there';
  const location = context?.location || 'home';
  const timeOfDay = context?.timeOfDay || '';

  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
    
    let userPrompt;
    if (userMessage && userMessage.trim()) {
      // Conversational mode: user has spoken
      userPrompt = `Context: location=${location}, timeOfDay=${timeOfDay}, preferredName=${preferredName}\n` +
        `User said: "${userMessage.trim()}"\n` +
        'Please respond naturally and helpfully, keeping it short (1-2 sentences).';
    } else {
      // Proactive mode: no user input, just greeting
      userPrompt = `Context: location=${location}, timeOfDay=${timeOfDay}, preferredName=${preferredName}\n` +
        'Please produce a single short proactive greeting and offer of help suitable for speaking aloud.';
    }

    const result = await model.generateContent([
      { role: 'user', parts: [{ text: SYSTEM_PROMPT }] },
      { role: 'user', parts: [{ text: userPrompt }] }
    ]);

    const text = result.response?.text?.() || result.response?.candidates?.[0]?.content?.parts?.[0]?.text || 'Hello, how can I help you today?';
    return res.json({ text });
  } catch (err) {
    return res.status(500).json({ error: 'Gemini request failed', details: String(err) });
  }
});

app.listen(port, () => {
  console.log(`Memo MVP server running on http://localhost:${port}`);
});


