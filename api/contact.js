// api/contact.js
const https = require('https');
const querystring = require('querystring');

export default function handler(req, res) {
    const access_key = process.env.WEB3FORMS_ACCESS_KEY;

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') return res.status(200).end();
    if (req.method !== 'POST') return res.status(405).json({ success: false });

    const { name, email, message, website, formId } = req.body;

    // Przygotowanie danych w formacie formularza (nie JSON)
    const postData = querystring.stringify({
        access_key: access_key,
        name: name,
        email: email,
        subject: `Zgłoszenie: ${formId || 'Kontakt'}`,
        message: `Strona: ${website || 'Brak'}\n\nWiadomość: ${message || '(brak)'}`,
        from_name: "Collytics WWW"
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
            const result = JSON.parse(body);
            if (result.success) {
                return res.status(200).json({ success: true, message: 'Wysłano!' });
            } else {
                // Jeśli tu nadal będzie błąd "Method not allowed", Web3Forms całkowicie blokuje Twój adres IP
                return res.status(502).json({ success: false, message: result.message });
            }
        });
    });

    request.on('error', () => res.status(500).json({ success: false }));
    request.write(postData);
    request.end();
}
