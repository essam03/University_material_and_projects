<?php
require 'connection.php';

// Prepared SQL statement
$sql = "INSERT INTO battery_recycling_appointments (date_time, battery_type, length, width, height, phone) VALUES (:date_time, :battery_type, :length, :width, :height, :phone)";

$statement = $pdo->prepare($sql);

// Data to be inserted
$date_time = '2023-10-01 14:00:00'; // Example datetime
$battery_type = 'Lead Acid'; // Example battery type
$length = 7.5; // Example length in inches
$width = 5; // Example width in inches
$height = 6; // Example height in inches
$phone = '123-456-7890'; // Example phone number

// Bind parameters and execute the statement
$statement->bindParam(":date_time", $date_time, PDO::PARAM_STR);
$statement->bindParam(":battery_type", $battery_type, PDO::PARAM_STR);
$statement->bindParam(":length", $length, PDO::PARAM_STR);
$statement->bindParam(":width", $width, PDO::PARAM_STR);
$statement->bindParam(":height", $height, PDO::PARAM_STR);
$statement->bindParam(":phone", $phone, PDO::PARAM_STR);

if($statement->execute()) {
    echo "Appointment inserted successfully.";
} else {
    echo "Failed to insert appointment.";
}

$pdo = null;
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
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
    <header>
        <a href="http://127.0.0.1:5500/Final%20assignmnet/codes/Home.html"><img src="logo.png" alt="logo"></a>
        <h1>Booking an appointment</h1>
    </header>
    <div class="grid">
        <div class="info">
            <img src="pic.jpg" alt="pic" class="pic"> <!-- Image with alt attribute for accessibility and SEO -->
                        <!-- SEO: Text content about the benefits of booking an appointment -->

            <p>Booking an appointment offers multiple benefits to customers. First, it adds convenience by allowing people to pick a time that suits them best, improving their overall experience. Second, it saves time; customers know they have a reserved slot, so they can plan their day without stressing about waiting in line. Lastly, appointments often lead to more personalized and attentive service because the providers can get ready ahead of time to meet the customer's needs.</p>
        </div>
        <div class="input-section">
            <h3>The kind of battery</h3>
            <input type="text" placeholder="Enter the type of the battery">
            <h3>The size of the battery</h3>
            <input type="text" placeholder="Enter the height">
            <input type="text" placeholder="Enter the width">
            <input type="text" placeholder="Enter the length">
        </div> <!-- Form input sections -->
        <div class="appointment-section"> <!-- Input fields for appointment details -->
            <h3>Enter a time for the appointment</h3>
            <input type="date" placeholder="Enter a suitable time for you">
            <input type="time" placeholder="Enter an hour">
            <h3>Enter your phone number</h3>
            <input type="tel" placeholder="Enter your phone number">
        </div>
        <button id="confirmBtn" type="submit">Confirm your reservation</button><!-- Button to confirm reservation -->
        <div id="alertBox" class="alert" role="alert" style="display:none;">  <!-- Alert box for reservation confirmation -->
            The appointment is resaerved
        </div>
    </div>
     <!-- JavaScript to show confirmation alert -->
    <script>
        // Get the button element by its id
        const confirmBtn = document.getElementById('confirmBtn');

        // Get the alert box element by its id
        const alertBox = document.getElementById('alertBox');

        // Add click event listener to the button
        confirmBtn.addEventListener('click', function() {
            // Show the alert box
            alertBox.style.display = 'block';
            alertBox.classList.add('alert-success');
        });
    </script>
</body>
</html>
