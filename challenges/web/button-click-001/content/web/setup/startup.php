<?php
    $servername = "db";
    $username = "buttonclick";
    $password = "buttonclick";
    $dbname = "buttonclickerdb";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully\r\n";

$sql = "CREATE TABLE IF NOT EXISTS buttonclicker_table
    (
        user_id INT NOT NULL AUTO_INCREMENT,
        session_key VARCHAR(255) NOT NULL,
        click_count INT NOT NULL,
        primary key (user_id)
     );";
$result = $conn->query($sql);
echo $result;
$conn->close();
?>