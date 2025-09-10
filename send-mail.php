<?php
// send-mail.php - Umieść ten plik w głównym katalogu strony

// Konfiguracja
$to_email = "hello@collytics.io";
$subject_prefix = "[Collytics Website] ";

// Nagłówki CORS (jeśli potrzebne)
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Sprawdzenie metody
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Metoda nie dozwolona']);
    exit;
}

// Pobranie danych z formularza
$data = json_decode(file_get_contents('php://input'), true);

// Walidacja danych
if (empty($data['name']) || empty($data['email']) || empty($data['message'])) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Wypełnij wszystkie wymagane pola']);
    exit;
}

// Sanityzacja danych
$name = filter_var($data['name'], FILTER_SANITIZE_STRING);
$email = filter_var($data['email'], FILTER_SANITIZE_EMAIL);
$message = filter_var($data['message'], FILTER_SANITIZE_STRING);

// Walidacja emaila
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Nieprawidłowy adres email']);
    exit;
}

// Sprawdzenie zgody
if (!isset($data['consent']) || !$data['consent']) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Musisz wyrazić zgodę na przetwarzanie danych']);
    exit;
}

// Przygotowanie wiadomości
$email_subject = $subject_prefix . "Nowa wiadomość od " . $name;

$email_body = "Nowa wiadomość z formularza kontaktowego Collytics.io\n\n";
$email_body .= "================================\n\n";
$email_body .= "Imię: " . $name . "\n";
$email_body .= "Email: " . $email . "\n";
$email_body .= "Data: " . date('Y-m-d H:i:s') . "\n\n";
$email_body .= "Wiadomość:\n";
$email_body .= "--------------------------------\n";
$email_body .= $message . "\n";
$email_body .= "--------------------------------\n\n";
$email_body .= "Zgoda na przetwarzanie danych: TAK\n";
$email_body .= "IP nadawcy: " . $_SERVER['REMOTE_ADDR'] . "\n";

// Nagłówki emaila
$headers = "From: " . $name . " <" . $email . ">\r\n";
$headers .= "Reply-To: " . $email . "\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

// Wysłanie emaila
if (mail($to_email, $email_subject, $email_body, $headers)) {
    // Opcjonalnie: zapisz do bazy danych lub pliku logów
    $log_entry = date('Y-m-d H:i:s') . " | " . $name . " | " . $email . " | Wiadomość wysłana\n";
    file_put_contents('contact_log.txt', $log_entry, FILE_APPEND | LOCK_EX);

    // Wysłanie potwierdzenia do nadawcy (opcjonalne)
    $confirmation_subject = "Potwierdzenie otrzymania wiadomości - Collytics";
    $confirmation_body = "Cześć " . $name . "!\n\n";
    $confirmation_body .= "Dziękujemy za kontakt! Otrzymaliśmy Twoją wiadomość i odpowiemy najszybciej jak to możliwe.\n\n";
    $confirmation_body .= "Pozdrawiamy,\n";
    $confirmation_body .= "Zespół Collytics\n\n";
    $confirmation_body .= "---\n";
    $confirmation_body .= "To jest automatyczna wiadomość. Nie odpowiadaj na ten email.";

    $confirmation_headers = "From: Collytics <noreply@collytics.io>\r\n";
    $confirmation_headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

    mail($email, $confirmation_subject, $confirmation_body, $confirmation_headers);

    // Sukces
    echo json_encode([
        'success' => true,
        'message' => 'Dziękujemy za wiadomość! Odpowiemy najszybciej jak to możliwe.'
    ]);
} else {
    // Błąd wysyłania
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie.'
    ]);
}
?>
