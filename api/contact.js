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

    // Walidacja
    if (!name || !email || !consent) {
        return res.status(400).json({ success: false, message: 'Brak wymaganych pól.' });
    }

    if (!access_key) {
        return res.status(500).json({ success: false, message: 'Błąd konfiguracji: brak klucza API.' });
    }

    // Formatowanie treści
    const content = `Formularz: ${formId || 'Kontakt'}\nImię: ${name}\nEmail: ${email}\nWWW: ${website || 'nie podano'}\n\nWiadomość:\n${message || '(brak)'}`;

    const data = JSON.stringify({
        access_key: access_key,
        name: name,
        email: email,
        subject: `[Collytics] Zgłoszenie od ${name}`,
        message: content,
    });

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
        let responseData = '';
        response.on('data', (chunk) => { responseData += chunk; });
        response.on('end', () => {
            const result = JSON.parse(responseData);
            if (result.success) {
                return res.status(200).json({ success: true, message: 'Wysłano pomyślnie!' });
            } else {
                return res.status(502).json({ success: false, message: 'Web3Forms zwrócił błąd.' });
            }
        });
    });

    request.on('error', (error) => {
        console.error('Błąd https.request:', error);
        return res.status(500).json({ success: false, message: 'Błąd krytyczny połączenia.' });
    });

    request.write(data);
    request.end();
}
