// api/send-mail.js
export default async function handler(req, res) {
  // Tylko POST
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  const { name, email, message, consent } = req.body;

  // Walidacja
  if (!name || !email || !message || !consent) {
    return res.status(400).json({
      success: false,
      message: 'Wypełnij wszystkie pola'
    });
  }

  try {
    // Opcja 1: Użyj zewnętrznego API (np. SendGrid, Resend)
    // Opcja 2: Użyj serwisu formularzy
    // Opcja 3: Zapisz do bazy danych

    // Tymczasowo - logowanie (w produkcji użyj prawdziwego serwisu)
    console.log('Nowa wiadomość:', { name, email, message });

    return res.status(200).json({
      success: true,
      message: 'Dziękujemy za wiadomość!'
    });
  } catch (error) {
    console.error('Błąd:', error);
    return res.status(500).json({
      success: false,
      message: 'Wystąpił błąd'
    });
  }
}
