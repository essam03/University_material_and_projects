<?php
session_start();

if(isset($_SESSION['privilleged'])){
    unset($_SESSION['privilleged']);
    
}

header("http://127.0.0.1:5500/Home.html");
    die();
?>