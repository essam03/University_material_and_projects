<?php
require 'connection.php';
if(isset($_POST['insert'])){

    $sql = "INSERT INTO appointment(kind_of_battery, length, height, width, date, time, phone) VALUES (:kind_of_battery, :length, :height, :width, :date, :time, :phone)";
    $statement = $pdo->prepare($sql);

    $kind_of_battery = $_POST['kind_of_battery'];
    $length = $_POST['length'];
    $height = $_POST['height'];
    $width = $_POST['width'];
    $date = $_POST['date'];
    $time = $_POST['time'];
    $phone = $_POST['phone'];
   
    

    $statement->bindParam(":kind_of_battery", $kind_of_battery, PDO::PARAM_STR);
    $statement->bindParam(":length", $length, PDO::PARAM_INT);
    $statement->bindParam(":height", $height, PDO::PARAM_INT);
    $statement->bindParam(":width", $width, PDO::PARAM_INT);
    $statement->bindParam(":date", $date, PDO::PARAM_STR);
    $statement->bindParam(":time", $time, PDO::PARAM_STR);
    $statement->bindParam(":phone", $phone, PDO::PARAM_STR);

    $statement->execute();
    $pdo = null;

    echo "New appointment has been added successfully";
}
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>booking an appointment</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        body {
            background-color: #93bc3f;
        }
        header {
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background-color: #cadcbf;
        }
        .pic {
            width: 100%;
            max-height: 500px;
        }
        .grid {
            padding: 20px;
            max-width: 1200px;
            margin: auto;
        }
        .info, .input-section, .appointment-section {
            margin-bottom: 20px;
        }
        button {
            color: #808080; 
            width: 100%;  
            height: 50px;
            border: none;
            cursor: pointer;
        }
        @media (min-width: 600px) {
            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-gap: 20px;
            }
            header, .info {
                grid-column: span 2;
            }
        }
    </style>
</head>
<body>
<form method="POST" action="">
    <header>
        <a href="http://127.0.0.1:5500/Final%20assignmnet/codes/Home.html"><img src="logo.png" alt="logo"></a>
        <h1>Booking an appointment</h1>
    </header>
    <div class="grid">
        <div class="info">
           <a href="http://127.0.0.1:5500/Final%20assignmnet/codes/Home.html"> <img src="pic.jpg" alt="pic" class="pic"> </a>
            <p>Booking an appointment offers multiple benefits to customers. First, it adds convenience by allowing people to pick a time that suits them best, improving their overall experience. Second, it saves time; customers know they have a reserved slot, so they can plan their day without stressing about waiting in line. Lastly, appointments often lead to more personalized and attentive service because the providers can get ready ahead of time to meet the customer's needs.</p>
        </div>
    <div class="input-section">
    <h3>The kind of battery</h3>
    <input type="text" name="kind_of_battery" placeholder="Enter the type of the battery">
    <h3>The size of the battery</h3>
    <input type="text" name="height" placeholder="Enter the height">
    <input type="text" name="width" placeholder="Enter the width">
    <input type="text" name="length" placeholder="Enter the length">
    </div>

<div class="appointment-section">
    <h3>Enter a time for the appointment</h3>
    <input type="date" name="date" placeholder="Enter a suitable time for you">
    <input type="time" name="time" placeholder="Enter an hour">
    <h3>Enter your phone number</h3>
    <input type="tel" name="phone" placeholder="Enter your phone number">
</div>

        <a href="http://127.0.0.1:5500/Final%20assignmnet/codes/Home.html"><button id="confirmBtn" type="submit">Confirm your reservation</button></a>
        <a href="http://localhost/Final%20assignmnet/php2/changing.php">
            <button id="changing" type="button">Show, edit or delete the appointment</button>
        </a>
    </div>
</body>
</html>