// api/contact.js
export default async function handler(req, res) {
  const access_key = process.env.WEB3FORMS_ACCESS_KEY;

  // Obsługa CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  const { name, email, message, website, consent, formId } = req.body;

  // Podstawowa walidacja (Imię i Email są zawsze wymagane)
  if (!name || !email) {
    return res.status(400).json({ success: false, message: 'Imię i email są wymagane.' });
  }

  // Walidacja zgody
  if (!consent) {
    return res.status(400).json({ success: false, message: 'Zgoda na przetwarzanie danych jest wymagana.' });
  }

  // Walidacja specyficzna dla formularza Audytu AI
  if (formId === 'AI Visibility Audit LP') {
    if (!website) {
      return res.status(400).json({ success: false, message: 'Adres strony WWW jest wymagany dla raportu.' });
    }
  } else {
    // Dla innych formularzy (np. kontakt) wiadomość jest wymagana
    if (!message) {
      return res.status(400).json({ success: false, message: 'Treść wiadomości jest wymagana.' });
    }
  }

  if (!access_key) {
      console.error('Błąd: Brak WEB3FORMS_ACCESS_KEY w ustawieniach Vercel.');
      return res.status(500).json({ success: false, message: 'Błąd konfiguracji serwera.' });
  }

  try {
    // Łączymy dane w jedną wiadomość dla Web3Forms
    const finalMessage = website 
      ? `DOMENA: ${website}\nWIADOMOŚĆ: ${message || '(brak dodatkowej treści)'}`
      : message;

    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        access_key: access_key,
        subject: formId || `Kontakt od ${name}`,
        from_name: name,
        email: email,
        message: finalMessage,
        to: 'hello@collytics.io'
      })
    });

    const result = await response.json();
    if (result.success) {
      return res.status(200).json({ success: true, message: 'Wiadomość wysłana!' });
    } else {
      throw new Error(result.message);
    }
  } catch (error) {
    return res.status(500).json({ success: false, message: 'Błąd wysyłania przez API.' });
  }
}
