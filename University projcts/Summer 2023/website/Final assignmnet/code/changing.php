<?php
require 'connection.php';
$sql="SELECT * FROM appointment";
$statement=$pdo->prepare($sql);
$statement->execute();
echo "<table style='border:1px solid; width:80%; text-align:center; margin:auto;'>";
echo "<tr>";
echo "<th> kind_of_battery</th>";
echo "<th> length </th>";
echo "<th> height </th>";
echo "<th> width </th>";
echo "<th> date </th>";
echo "<th> time </th>";
echo "<th> phone </th>";
echo "</tr>";
$data=$statement->fetchAll();
foreach ($data as $row) {
    echo "<tr>".
    "<td>" . $row['kind_of_battery']. " </td>".
    " <td> ". $row['length'] . " </td>".
    " <td> ". $row['height'] . " </td>".
    " <td> ". $row['width'] . " </td>". 
    " <td> ". $row['date'] . " </td>".
    " <td> ". $row['time'] . " </td>".
    "<td>" . $row['phone'] . "</td>".    
     "<td><a href='http://localhost/Final%20assignmnet/php2/editAppointment.php?id=". htmlspecialchars($row['id']). "'> edit </a></td>".
    "<td> <a href='deleteAppointment.php?id=". htmlspecialchars($row['id']). "'> delete </a> </td>".
    "</tr>";
}

echo "</table>";
$pdo=null;
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>changing appointment</title>
    <style>
    body {
        background-color: #93bc3f;
        margin: 0;
        display: grid;
        place-items: center;
        height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    table {
        width: 80%;
        border: 1px solid #000;
        text-align: center;
    }
    th, td {
        padding: 8px;
        border: 1px solid #000;
    }
</style>
</head>
<body>
<img src="logo.png" alt="recyling" id="logo">
<a href='http://127.0.0.1:5500/Home.html'><button> logout</button></a>
</body>
</html>