// api/contact.js
export default async function handler(req, res) {
  const access_key = process.env.WEB3FORMS_ACCESS_KEY;

  // Nagłówki CORS - ważne dla Vercel
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  const { name, email, message, website, consent, formId } = req.body;

  // Sprawdzenie klucza
  if (!access_key) {
    return res.status(500).json({ success: false, message: 'Błąd konfiguracji: Brak klucza API.' });
  }

  try {
    // Wysyłka w formacie JSON (wymaga planu Pro przy wysyłce z serwera)
    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        access_key: access_key,
        from_name: "Collytics WWW",
        subject: website ? `[AUDYT AI] Raport dla ${name}` : `[KONTAKT] Wiadomość od ${name}`,
        name: name,
        email: email,
        // Łączymy pola w czytelną treść
        message: `Formularz: ${formId || 'Ogólny'}\nStrona WWW: ${website || 'N/A'}\n\nWiadomość:\n${message || '(Brak dodatkowej treści)'}`,
      })
    });

    const result = await response.json();

    if (result.success) {
      return res.status(200).json({ 
        success: true, 
        message: 'Dziękujemy! Twoja wiadomość została wysłana.' 
      });
    } else {
      // Jeśli Web3Forms nadal odrzuca, wyślemy dokładny błąd do konsoli Vercel
      console.error('Web3Forms Error:', result);
      return res.status(502).json({ 
        success: false, 
        message: `Błąd Web3Forms: ${result.message}` 
      });
    }
  } catch (error) {
    console.error('Krytyczny błąd API:', error);
    return res.status(500).json({ 
      success: false, 
      message: 'Wystąpił błąd podczas komunikacji z serwerem poczty.' 
    });
  }
}
