<?php
session_start();
$servername = "172.17.0.4";
$username = "buttonclick";
$password = "buttonclick";



// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";
?>