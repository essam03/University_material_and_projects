<?php
$host = 'localhost';
$dbname = 'recyclo';
$user = 'root';
$password = ''; // if there is no password, it should be an empty string

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $password);
    echo "Connected successfully";
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>
