<?php
require 'connection.php';
$sql="DELETE FROM appointment WHERE id=:id";
$id=$_GET['id'];
$statement=$pdo->prepare($sql);
$statement->bindParam(":id",$id, PDO::PARAM_INT);
$statement->execute();
$pdo=null;

echo "employee with id $id is deleted </br> ";


?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Delete appointment</title>
  <style>
    body {
      background-color: #93bc3f;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    a {
      font-size: 18px;
      color: white; /* Adjust as necessary */
    }
  </style>
</head>
<body>
  <a href="http://localhost/Final%20assignmnet/php2/changing.php">View Appointment</a>
</body>
</html>
