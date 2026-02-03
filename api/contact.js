// api/contact.js
const https = require('https');
const querystring = require('querystring');

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

    // Walidacja podstawowa
    if (!name || !email || !consent) {
        return res.status(400).json({ success: false, message: 'Wypełnij wymagane pola.' });
    }

    // Przygotowanie danych w formacie formularza (urlencoded) - to klucz do obejścia blokady
    const postData = querystring.stringify({
        access_key: access_key,
        from_name: "Collytics WWW",
        subject: website ? `[AUDYT AI] Zgłoszenie od ${name}` : `[KONTAKT] Wiadomość od ${name}`,
        name: name,
        email: email,
        message: `Typ: ${formId || 'Kontakt'}\nWWW: ${website || 'Brak'}\n\nWiadomość: ${message || 'Brak dodatkowej treści'}`,
        to: 'hello@collytics.io'
    });

    const options = {
        hostname: 'api.web3forms.com',
        path: '/submit',
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
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
                return res.status(500).json({ success: false, message: 'Błąd odpowiedzi serwera.' });
            }
        });
    });

    request.on('error', (err) => {
        console.error('Błąd połączenia:', err);
        return res.status(500).json({ success: false, message: 'Błąd połączenia z API.' });
    });

    request.write(postData);
    request.end();
}
