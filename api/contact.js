// api/contact.js
export default async function handler(req, res) {
  const access_key = process.env.WEB3FORMS_ACCESS_KEY;

  // Obsługa nagłówków CORS dla Vercel
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

  // Walidacja danych
  if (!name || !email || !consent) {
    return res.status(400).json({ success: false, message: 'Wymagane pola nie zostały wypełnione' });
  }

  if (!access_key) {
    console.error('Błąd: Brak WEB3FORMS_ACCESS_KEY w środowisku Vercel');
    return res.status(500).json({ success: false, message: 'Błąd konfiguracji serwera' });
  }

  try {
    // Wysyłka do Web3Forms (teraz dozwolona w planie Pro)
    const web3formsResponse = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        access_key: access_key,
        subject: website ? `[AUDYT AI] Nowe zgłoszenie od ${name}` : `[KONTAKT] Nowa wiadomość od ${name}`,
        from_name: name,
        email: email,
        message: website ? `Strona WWW: ${website}\n\nWiadomość: ${message || '(brak treści)'}` : message,
        to: 'hello@collytics.io'
      })
    });

    const result = await web3formsResponse.json();

    if (result.success) {
      return res.status(200).json({
        success: true,
        message: 'Dziękujemy! Twoja wiadomość została wysłana.'
      });
    } else {
      throw new Error(result.message || 'Błąd API Web3Forms');
    }

  } catch (error) {
    console.error('Błąd wysyłania formularza:', error);
    return res.status(500).json({
      success: false,
      message: 'Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie.'
    });
  }
}
