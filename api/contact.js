// api/contact.js
// Poprawiona wersja z Web3Forms i kluczem ze zmiennej środowiskowej

export default async function handler(req, res) {
  // === NOWOŚĆ: POBIERANIE KLUCZA Z ENV ===
  const access_key = process.env.WEB3FORMS_ACCESS_KEY;
  // ======================================

  // Obsługa CORS (pozostałe rzeczy pominięte dla zwięzłości)
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

  const { name, email, message, consent } = req.body;

  // Walidacja (pozostaje bez zmian)
  if (!name || !email || !message) {
    return res.status(400).json({ success: false, message: 'Wszystkie pola są wymagane' });
  }

  if (!consent) {
    return res.status(400).json({ success: false, message: 'Zgoda na przetwarzanie danych jest wymagana' });
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return res.status(400).json({ success: false, message: 'Nieprawidłowy adres email' });
  }
  
  // === NOWOŚĆ: Sprawdzenie, czy klucz jest dostępny ===
  if (!access_key) {
      console.error('Błąd konfiguracji: brak WEB3FORMS_ACCESS_KEY.');
      return res.status(500).json({
          success: false,
          message: 'Wystąpił błąd konfiguracji serwera. Spróbuj ponownie później.'
      });
  }
  // =================================================

  try {
    // Wysyłka przez Web3Forms
    const web3formsResponse = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        access_key: access_key, // UŻYWAMY ZMIENNEJ ENV
        subject: `Nowa wiadomość od ${name}`,
        from_name: name,
        email: email,
        message: message,
        to: 'hello@collytics.io'
      })
    });

    const result = await web3formsResponse.json();

    if (result.success) {
      return res.status(200).json({
        success: true,
        message: 'Dziękujemy za wiadomość! Odpowiemy najszybciej jak to możliwe.'
      });
    } else {
      // Jeśli Web3Forms zwraca błąd, zgłaszamy go
      throw new Error(result.message || 'Błąd API Web3Forms: Nie udało się wysłać wiadomości.');
    }

  } catch (error) {
    console.error('Błąd przetwarzania formularza:', error);
    return res.status(500).json({
      success: false,
      message: 'Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie.'
    });
  }
}
