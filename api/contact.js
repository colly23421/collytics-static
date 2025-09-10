// api/contact.js
// Poprawiona wersja z Web3Forms

export default async function handler(req, res) {
  // Obsługa CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

  // Obsługa OPTIONS request
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Tylko POST
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  const { name, email, message, consent } = req.body;

  // Walidacja
  if (!name || !email || !message) {
    return res.status(400).json({
      success: false,
      message: 'Wszystkie pola są wymagane'
    });
  }

  if (!consent) {
    return res.status(400).json({
      success: false,
      message: 'Zgoda na przetwarzanie danych jest wymagana'
    });
  }

  // Walidacja email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({
      success: false,
      message: 'Nieprawidłowy adres email'
    });
  }

  try {
    // Wysyłka przez Web3Forms
    const web3formsResponse = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        access_key: '4269c53d-7b3e-4fb7-a61a-e4a561eeda36',
        subject: `Nowa wiadomość od ${name}`,
        from_name: name,
        email: email,
        message: message,
        to: 'hello@collytics.io' // Dodaj adres docelowy
      })
    });

    const result = await web3formsResponse.json();

    // Logowanie dla debugowania
    console.log('Web3Forms response:', result);
    console.log('=== NOWA WIADOMOŚĆ Z FORMULARZA ===');
    console.log('Imię:', name);
    console.log('Email:', email);
    console.log('Wiadomość:', message);
    console.log('Data:', new Date().toISOString());
    console.log('=====================================');

    // Sprawdź czy wysłano pomyślnie
    if (result.success) {
      return res.status(200).json({
        success: true,
        message: 'Dziękujemy za wiadomość! Odpowiemy najszybciej jak to możliwe.'
      });
    } else {
      throw new Error(result.message || 'Web3Forms error');
    }

  } catch (error) {
    console.error('Błąd przetwarzania formularza:', error);
    return res.status(500).json({
      success: false,
      message: 'Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie.'
    });
  }
}
