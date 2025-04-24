<?php
$id = 0;
require 'connection.php';

if (isset($_POST['update'])) {
    $sql = "UPDATE appointment SET 
        kind_of_battery=:kind_of_battery, 
        length=:length, 
        height=:height, 
        width=:width, 
        date=:date, 
        time=:time, 
        phone=:phone
    WHERE id=:id";

    $statement = $pdo->prepare($sql);
    
    $kind_of_battery = $_POST['kind_of_battery'];
    $length = $_POST['length'];
    $height = $_POST['height'];
    $width = $_POST['width'];
    $date = $_POST['date'];
    $time = $_POST['time'];
    $phone = $_POST['phone'];
    $id = $_GET['id'];
    
    $statement->bindParam(':kind_of_battery', $kind_of_battery, PDO::PARAM_STR);
    $statement->bindParam(':length', $length, PDO::PARAM_STR);
    $statement->bindParam(':height', $height, PDO::PARAM_STR);
    $statement->bindParam(':width', $width, PDO::PARAM_STR);
    $statement->bindParam(':date', $date, PDO::PARAM_STR);
    $statement->bindParam(':time', $time, PDO::PARAM_STR);
    $statement->bindParam(':phone', $phone, PDO::PARAM_INT);
    $statement->bindParam(':id', $id, PDO::PARAM_INT);

    $statement->execute();
    echo "appointment with id $id is successfully updated <br>";
}

$sql = "SELECT * FROM appointment WHERE id=:id";
$statement = $pdo->prepare($sql);
$statement->bindParam(':id', $id, PDO::PARAM_INT);
$statement->execute();
$data = $statement->fetchAll();

echo "<h2>";
foreach ($data as $row) {
    echo $row['kind_of_battery'] . ' ' . $row['length'] . ' ' . $row['height'] . ' ' . $row['width'] . ' ' . $row['date'] . ' ' . $row['time'] . ' ' . $row['phone'];
    echo "<br>";
}
echo "</h2>";
$pdo = null;
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Booking an appointment</title>
    <style>
        body {
            background-color: #93bc3f;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
    </style>
</head>
<body>
<form action="/action_page.php">

<label for="kind_of_battery">Kind of Battery:</label><br>
<input type="text" id="kind_of_battery" name="kind_of_battery" value="<?php echo $kind_of_battery; ?>"><br>

<label for="length">Length:</label><br>
<input type="text" id="length" name="length" value="<?php echo $length; ?>"><br>

<label for="height">Height:</label><br>
<input type="text" id="height" name="height" value="<?php echo $height; ?>"><br>

<label for="width">Width:</label><br>
<input type="text" id="width" name="width" value="<?php echo $width; ?>"><br>

<label for="date">Date:</label><br>
<input type="text" id="date" name="date" value="<?php echo $date; ?>"><br>

<label for="time">Time:</label><br>
<input type="text" id="time" name="time" value="<?php echo $time; ?>"><br>

<label for="phone">Phone:</label><br>
<input type="text" id="phone" name="phone" value="<?php echo $phone; ?>"><br><br>

<input type="submit" value="Submit">
</form>

<a href="changing.php"> view your appointment </a>
</body>
</html>
