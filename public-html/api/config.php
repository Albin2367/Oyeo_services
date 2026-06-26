<?php
// config.php
define('DB_HOST', 'localhost');
define('DB_NAME', 'VOTRE_NOM_DE_BASE');
define('DB_USER', 'VOTRE_UTILISATEUR');
define('DB_PASS', 'VOTRE_MOT_DE_PASSE');

try {
    $bdd = new PDO("mysql:host=".DB_HOST.";dbname=".DB_NAME.";charset=utf8", DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);
} catch (Exception $e) {
    header('Content-Type: application/json');
    echo json_encode(['success' => false, 'message' => 'Erreur de connexion serveur.']);
    exit;
}