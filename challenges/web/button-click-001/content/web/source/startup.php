<?php
$servername = "172.17.0.4";
$username = "buttonclick";
$password = "buttonclick";

// Create connection
$conn = new mysqli($servername, $username, $password);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully\r\n";

$sql = "CREATE TABLE IF NOT EXISTS buttonclicker_table (
    session_key INT(100000) UNSIGNED AUTO_INCREMENT PRIMARY_KEY,
    session_id text(),
    click_count INT()
)";
if ($conn->query($sql) === TRUE) {
    echo "Created Tables\r\n";
}

$sql = "SHOW COLUMNS FROM buttonclicker_table";
if ($conn->query($sql) === TRUE) {
    echo "SHOWING TABLES\r\n";
}
?>