<?php
require 'connection.php';
$sql = "INSERT INTO registration (Fname, Lname, date_of_birth, phone, username, password) VALUES (:Fname, :Lname, :date_of_birth, :phone, :username, :password)";

$statement = $pdo->prepare($sql);

$Fname = 'math';
$Lname = 'fox';
$date_of_birth = '2/5/2000';
$phone = '0796548371';
$username = 'math';
$password = 'math20';

$statement->bindParam(":Fname", $Fname, PDO::PARAM_STR);
$statement->bindParam(":Lname", $Lname, PDO::PARAM_STR);
$statement->bindParam(":date_of_birth", $date_of_birth, PDO::PARAM_STR);
$statement->bindParam(":phone", $phone, PDO::PARAM_INT);
$statement->bindParam(":username", $username, PDO::PARAM_STR);
$statement->bindParam(":password", $password, PDO::PARAM_STR);

$statement->execute();
$pdo = null;

echo "it's done";
?>
