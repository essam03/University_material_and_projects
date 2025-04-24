<?php
require 'connection.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    
$sql = "INSERT INTO registration (Fname, Lname, date_of_birth, phone, username, password) VALUES (:Fname, :Lname, :date_of_birth, :phone, :username, :password)";
$statement=$pdo->prepare($sql);

$Fname = $_POST['Fname'];
$Lname = $_POST['Lname'];
$date_of_birth = $_POST['date_of_birth'];
$phone = $_POST['phone'];
$username = $_POST['username'];
$password = $_POST['password'];


$statement->bindParam(':Fname', $Fname, PDO::PARAM_STR);
    $statement->bindParam(':Lname', $Lname, PDO::PARAM_STR);
    $statement->bindParam(':date_of_birth', $date_of_birth, PDO::PARAM_STR);
    $statement->bindParam(':phone', $phone, PDO::PARAM_INT);
    $statement->bindParam(':username', $username, PDO::PARAM_STR);
    $statement->bindParam(':password', $password, PDO::PARAM_STR);
    $statement->execute();

    echo "new user is added succefully, go to login ";

}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        }
        body {
            background-color: #93bc3f;
        }
        .general-design {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            background-color: #cadcbf;
        }
        img#logo {
            display: block;
            margin: auto;
        }
        h3 {
            margin-top: 20px;
        }
        input[type="text"],
        input[type="date"],
        input[type="password"] {
            width: 100%;
            height: 40px;
            margin-bottom: 20px;
            padding-left: 10px;
        }
        button {
            width: 100%;
            height: 40px;
            font-size: 30px;
            background-color: #808080;
            color: white;
            border: none;
        }
    </style>
</head>
<body>
<form action="" method="POST">
    <div class="general-design">
    
        <img src="logo.png" alt="recycling" id="logo">
        <h3>Fname</h3>
        <input type="text" name="Fname" placeholder="Enter your first name...">
        <h3>Lname</h3>
        <input type="text" name="Lname" placeholder="Enter your last name...">
        <h3>Date of Birth</h3>
        <input type="date" name="date_of_birth" placeholder="Enter your age...">
        <h3>Phone</h3>
        <input type="text" name="phone" placeholder="Enter your phone...">
        <h3>Username</h3>
        <input type="text" name="username" placeholder="Enter your username...">
        <h3>Password</h3>
        <input type="password" name="password" placeholder="Enter your password...">
        <h3>Password Verification</h3>
        <input type="password" name="password_verification" placeholder="Enter your password again...">
        <button type="submit">Submit</button>
    
    </div>
</from>
</body>
</html>
