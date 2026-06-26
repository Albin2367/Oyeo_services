<?php
// api/contact.php
header('Content-Type: application/json');
require_once '../config.php';

// Récupérer le contenu JSON envoyé par vos scripts JS
$json = file_get_contents('php://input');
$data = json_decode($json, true);

if (!$data) {
    echo json_encode(['success' => false, 'message' => 'Données invalides.']);
    exit;
}

// Extraction et nettoyage des données
$email = filter_var(trim($data['email'] ?? ''), FILTER_VALIDATE_EMAIL);
$first_name = htmlspecialchars(trim($data['first_name'] ?? ''));
$last_name = htmlspecialchars(trim($data['last_name'] ?? ''));
$phone = htmlspecialchars(trim($data['phone'] ?? ''));
$service = htmlspecialchars(trim($data['service'] ?? ''));
$message = htmlspecialchars(trim($data['message'] ?? ''));

if (!$email || !$first_name || !$message) {
    echo json_encode(['success' => false, 'message' => 'Champs obligatoires manquants ou invalides.']);
    exit;
}

// Détecter automatiquement si c'est le formulaire détaillé ou simple
$type_formulaire = (strpos($message, 'formulaire Dédié :') !== false) ? 'prestation' : 'contact';

// Extraction des champs de structure si présents (Ville, adresse)
$ville = null;
$adresse = null;

if ($type_formulaire === 'prestation') {
    // Analyse rapide du message formaté pour remplir les colonnes BDD proprement
    if (preg_re(/^- Ville :\s*(.*)$/m, $message, $matches)) $ville = htmlspecialchars(trim($matches[1]));
    if (preg_re(/^- Adresse\/Zone :\s*(.*)$/m, $message, $matches)) $adresse = htmlspecialchars(trim($matches[1]));
}

try {
    $stmt = $bdd->prepare("INSERT INTO oyeo_contacts (type_formulaire, nom, prenom, email, telephone, service, ville, adresse, message) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
    $stmt->execute([$type_formulaire, $last_name, $first_name, $email, $phone, $service, $ville, $adresse, $message]);
    
    echo json_encode([
        'success' => true, 
        'message' => 'Votre demande a bien été enregistrée avec succès. Un conseiller vous recontactera rapidement.'
    ]);
} catch (Exception $e) {
    echo json_encode(['success' => false, 'message' => 'Une erreur interne est survenue. Veuillez réessayer.']);
}