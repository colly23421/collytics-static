// api/contact.js
const https = require('https');

export default function handler(req, res) {
    const access_key = process.env.WEB3FORMS_ACCESS_KEY;

    // Nagłówki CORS dla Vercel
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

    const { name, email, message, website, consent, formId } = req.body;

    // Prosta walidacja
    if (!name || !email || !consent) {
        return res.status(400).json({ success: false, message: 'Wypełnij wymagane pola.' });
    }

    // Przygotowanie danych do wysyłki
    const formData = {
        access_key: access_key,
        from_name: "Collytics",
        subject: website ? `Nowy Audyt AI: ${name}` : `Kontakt: ${name}`,
        name: name,
        email: email,
        // Łączymy wszystkie informacje w jedno pole 'message'
        message: `Typ: ${formId || 'Kontakt'}\nWWW: ${website || 'Brak'}\n\nWiadomość: ${message || 'Brak treści'}`
    };

    const data = JSON.stringify(formData);

    const options = {
        hostname: 'api.web3forms.com',
        path: '/submit',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length
        }
    };

    const request = https.request(options, (response) => {
        let responseBody = '';
        response.on('data', (chunk) => { responseBody += chunk; });
        response.on('end', () => {
            try {
                const result = JSON.parse(responseBody);
                if (result.success) {
                    return res.status(200).json({ success: true, message: 'Wiadomość wysłana!' });
                } else {
                    // Wyświetli dokładny błąd od Web3Forms w logach Vercel
                    console.error('Błąd Web3Forms:', result);
                    return res.status(502).json({ 
                        success: false, 
                        message: `Błąd Web3Forms: ${result.message || 'Nieznany błąd'}` 
                    });
                }
            } catch (e) {
                return res.status(500).json({ success: false, message: 'Błąd przetwarzania odpowiedzi.' });
            }
        });
    });

    request.on('error', (err) => {
        console.error('Błąd połączenia:', err);
        return res.status(500).json({ success: false, message: 'Błąd połączenia z serwerem poczty.' });
    });

    request.write(data);
    request.end();
}
