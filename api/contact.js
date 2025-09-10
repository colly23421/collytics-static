export default function handler(req, res) {
  if (req.method === 'POST') {
    console.log('Otrzymano:', req.body);
    res.status(200).json({ success: true, message: 'Wiadomość otrzymana!' });
  } else {
    res.status(405).json({ success: false, message: 'Method not allowed' });
  }
}
