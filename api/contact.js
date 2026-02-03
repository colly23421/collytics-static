// api/contact.js
const https = require('https');

export default function handler(req, res) {
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

    const { name, email, message, website, consent, formId } = req.body;

    if (!access_key) {
        return res.status(500).json({ success: false, message: 'Błąd konfiguracji: brak klucza API.' });
    }

    // Przygotowanie danych do wysyłki
    const postData = JSON.stringify({
        access_key: access_key,
        name: name,
        email: email,
        subject: website ? `[AUDYT AI] Nowe zgłoszenie: ${name}` : `[KONTAKT] Wiadomość od ${name}`,
        message: `Typ: ${formId || 'Kontakt'}\nWWW: ${website || 'Brak'}\n\nWiadomość: ${message || 'Brak dodatkowej treści'}`,
        from_name: "Collytics WWW"
    });

    const options = {
        hostname: 'api.web3forms.com',
        path: '/submit',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
        }
    };

    const request = https.request(options, (response) => {
        let body = '';
        response.on('data', (chunk) => body += chunk);
        response.on('end', () => {
            try {
                const result = JSON.parse(body);
                if (result.success) {
                    return res.status(200).json({ success: true, message: 'Wiadomość wysłana!' });
                } else {
                    return res.status(502).json({ success: false, message: result.message });
                }
            } catch (e) {
                return res.status(500).json({ success: false, message: 'Błąd przetwarzania odpowiedzi.' });
            }
        });
    });

    request.on('error', (err) => {
        console.error('Błąd połączenia z Web3Forms:', err);
        return res.status(500).json({ success: false, message: 'Błąd komunikacji z serwerem poczty.' });
    });

    request.write(postData);
    request.end();
}
