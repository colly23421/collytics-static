// api/contact.js
export default async function handler(req, res) {
  const access_key = process.env.WEB3FORMS_ACCESS_KEY;

  // Nagłówki CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  try {
    const { name, email, message, website, consent, formId } = req.body;

    // 1. Walidacja podstawowa
    if (!name || !email || !consent) {
      return res.status(400).json({ 
        success: false, 
        message: 'Imię, email oraz zgoda są wymagane.' 
      });
    }

    // 2. Sprawdzenie klucza API
    if (!access_key) {
      console.error('BŁĄD: Brak WEB3FORMS_ACCESS_KEY w Environment Variables na Vercel.');
      return res.status(500).json({ 
        success: false, 
        message: 'Serwer nie jest skonfigurowany do wysyłki (brak klucza).' 
      });
    }

    // 3. Przygotowanie czytelnej treści dla Web3Forms
    // Tworzymy tekst, który Web3Forms przyjmie bez błędów strukturalnych
    let content = `Nowe zgłoszenie: ${formId || 'Kontakt ogólny'}\n`;
    content += `---------------------------\n`;
    content += `Imię: ${name}\n`;
    content += `Email: ${email}\n`;
    if (website) content += `Strona WWW: ${website}\n`;
    content += `\nWiadomość:\n${message || '(Brak treści)'}`;

    // 4. Wysyłka do Web3Forms
    const response = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        access_key: access_key,
        from_name: "Collytics WWW",
        subject: website ? `[AUDYT AI] Zgłoszenie od ${name}` : `[KONTAKT] Wiadomość od ${name}`,
        name: name,
        email: email,
        message: content, // Przekazujemy sformatowany tekst
        to: 'hello@collytics.io'
      })
    });

    const result = await response.json();

    if (result.success) {
      return res.status(200).json({ 
        success: true, 
        message: 'Dziękujemy! Wiadomość została wysłana.' 
      });
    } else {
      console.error('Błąd Web3Forms:', result);
      return res.status(502).json({ 
        success: false, 
        message: 'Błąd dostawcy usług wysyłkowych. Spróbuj później.' 
      });
    }

  } catch (error) {
    console.error('Błąd krytyczny API:', error);
    return res.status(500).json({ 
      success: false, 
      message: 'Wystąpił błąd krytyczny serwera.' 
    });
  }
}
