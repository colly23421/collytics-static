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

  // Pobieramy wszystkie możliwe pola z różnych formularzy
  const { name, email, message, website, consent, formId } = req.body;

  // Podstawowa walidacja (wspólna dla wszystkich formularzy)
  if (!name || !email) {
    return res.status(400).json({ success: false, message: 'Imię i adres email są wymagane.' });
  }

  // Specyficzna walidacja dla formularza Audytu AI (musi mieć website)
  if (formId === 'AI Visibility Audit LP' && !website) {
    return res.status(400).json({ success: false, message: 'Adres strony WWW jest wymagany dla raportu.' });
  }

  // Specyficzna walidacja dla standardowego kontaktu (musi mieć message, jeśli nie jest to audyt)
  if (formId !== 'AI Visibility Audit LP' && !message) {
    return res.status(400).json({ success: false, message: 'Wpisz treść wiadomości.' });
  }

  if (!consent) {
    return res.status(400).json({ success: false, message: 'Zgoda na przetwarzanie danych jest wymagana.' });
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ success: false, message: 'Nieprawidłowy adres email.' });
  }
  
  if (!access_key) {
      console.error('Błąd konfiguracji: brak WEB3FORMS_ACCESS_KEY.');
      return res.status(500).json({
          success: false,
          message: 'Wystąpił błąd konfiguracji serwera.'
      });
  }

  try {
    // Przygotowanie treści wiadomości dla Web3Forms
    // Jeśli jest website, dodajemy go do treści
    const fullMessage = website 
      ? `Strona WWW: ${website}\n\nWiadomość: ${message || '(brak dodatkowej treści)'}`
      : message;

    const web3formsResponse = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        access_key: access_key,
        subject: formId || `Nowa wiadomość od ${name}`,
        from_name: name,
        email: email,
        message: fullMessage,
        to: 'hello@collytics.io'
      })
    });

    const result = await web3formsResponse.json();

    if (result.success) {
      return res.status(200).json({
        success: true,
        message: 'Dziękujemy! Twoja wiadomość została wysłana pomyślnie.'
      });
    } else {
      throw new Error(result.message || 'Błąd API Web3Forms');
    }

  } catch (error) {
    console.error('Błąd przetwarzania formularza:', error);
    return res.status(500).json({
      success: false,
      message: 'Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie.'
    });
  }
}
