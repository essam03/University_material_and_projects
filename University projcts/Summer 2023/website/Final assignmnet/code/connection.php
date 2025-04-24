<?php
$host = 'localhost';
$dbname = 'recyclo';
$user = 'root';
$password = ''; // if there is no password, it should be an empty string

$pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $password);
echo "Connected successfully";
?>
