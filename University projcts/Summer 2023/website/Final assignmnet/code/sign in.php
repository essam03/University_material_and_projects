<?php
session_start();
require 'connection.php';

if(isset($_POST['login'])){
    $sql="SELECT * from registration where username=:username and password=:password";
    $statement=$pdo->prepare($sql);
    $username=$_POST['username'];
    $password=$_POST['password'];

    $statement->bindParam(":username",$username,PDO::PARAM_STR);
    $statement->bindParam(":password",$password,PDO::PARAM_STR);
    $statement->execute();
    $count=$statement->rowCount();
    if($count==1){
        $_SESSION['privilleged']=$username;
        header("http://localhost/Final%20assignmnet/php2/booking.php");
    }else{
        echo "Invalid username or password";
    }
    $pdo=null;

}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body {
            background-color: #93bc3f;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background-color: #cadcbf;
            padding: 20px;
            text-align: center;
        }
        img#logo {
            max-width: 100%;
            height: auto;
            margin: auto;
        }
        h3 {
            margin: 20px 0;
        }
        input {
            width: 100%;
            height: 40px;
            margin: 10px 0;
        }
        button {
            width: 100%;
            height: 60px;
            font-size: 30px;
            background-color: #808080;
            color: white;
            border: none;
            margin: 10px 0;
        }
        a#forget {
            display: inline-block;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="logo.png" alt="recycling" id="logo"> <!-- SEO: Logo with alt attribute for accessibility and SEO -->
        <h3>Username</h3>
        <input type="text" name="username" placeholder="Enter your username..."><!-- SEO: Input fields for username with clear labels -->
        <h3>Password</h3>
        <input type="password" name="password" placeholder="Enter your password..."><!-- SEO: Input field for password with clear label -->
       <a href="http://localhost/Final%20assignmnet/php2/booking.php"> <button type="submit">Login</button></a><!-- SEO: Button for user login with clear text -->
        <a href="http://localhost/Final%20assignmnet/php/sign%20in.php"> <!-- SEO: Button for user registration with clear text -->
            <button type="button">Register</button>
        </a>
    </div>
</body>
</html>
