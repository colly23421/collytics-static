// api/contact.js
export default async function handler(req, res) {
  const access_key = process.env.WEB3FORMS_ACCESS_KEY;

  // Nagłówki CORS niezbędne dla Vercel
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ success: false, message: 'Method not allowed' });

  const { name, email, message, website, consent, formId } = req.body;

  if (!access_key) return res.status(500).json({ success: false, message: 'Błąd konfiguracji: Brak klucza API.' });

  try {
    // Wysyłka JSON - dozwolona TYLKO w planie Pro dla żądań z serwera
    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        access_key: access_key,
        from_name: "Collytics WWW",
        subject: website ? `[AUDYT AI] Nowe zgłoszenie: ${name}` : `[KONTAKT] Wiadomość od ${name}`,
        name: name,
        email: email,
        message: `Formularz: ${formId || 'Ogólny'}\nStrona WWW: ${website || 'Brak'}\n\nWiadomość:\n${message || '(brak treści)'}`,
      })
    });

    const result = await response.json();

    if (result.success) {
      return res.status(200).json({ success: true, message: 'Wiadomość wysłana!' });
    } else {
      // Jeśli Web3Forms nadal zwraca błąd, zobaczysz go w logach Vercel
      console.error('Web3Forms Error:', result);
      return res.status(502).json({ success: false, message: result.message });
    }
  } catch (error) {
    return res.status(500).json({ success: false, message: 'Błąd połączenia z serwerem poczty.' });
  }
}
