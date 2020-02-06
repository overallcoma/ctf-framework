<?php
session_start();
$servername = "db";
$username = "buttonclick";
$password = "buttonclick";
$dbname = "buttonclickerdb";

// print $servername;
// print $username;
// print $password;
// print $dbname;
$session_id = session_id();

echo "<br>";
// echo $session_id;
echo "<br>";

$conn = new mysqli($servername, $username, $password, $dbname);


$session_clickcount_query = "SELECT click_count FROM buttonclicker_table WHERE session_key = '$session_id' LIMIT 1;";
// echo $session_clickcount_query;
$result = $conn->query($session_clickcount_query);
while ($row = $result->fetch_assoc()) {
    // echo "<br>";
    // echo $row["user_id"];
    // echo "<br>";
    // echo $row["session_key"];
    // echo "<br>";
    echo $row["click_count"];
    echo "<br>";
}
if ($result->mysqli_num_rows > 0) {
        $clickcount = $result;
        print "COLD POTATO";
    }
else {
    $clickcount = 0;
    $create_record_query = "INSERT INTO buttonclicker_table (session_key, click_count) VALUES ('$session_id',0);";
    $conn->query($create_record_query);
}

function thebutton($post_value) {
    $servername = "db";
    $username = "buttonclick";
    $password = "buttonclick";
    $dbname = "buttonclickerdb";
    // echo $post_value;
    $conn = new mysqli($servername, $username, $password, $dbname);
    $session_add_click = "UPDATE buttonclicker_table SET click_count = click_count + 1 WHERE session_key = '$post_value';";
    echo $session_session_add_click;
    $result = $conn->query($session_add_click);
    // $conn.close();
}


$conn->close();
?>

<form method="post">
        <input type="hidden" name="top_secret_action" id="top_secret_action" value="<?php echo session_id(); ?>" >
        <input type="submit" name="thebutton" class="button" value="Click The Button!" >
</form>

<?php
    if(isset($_REQUEST['thebutton']))
    {
        echo "<div>";
        $post_value = $_POST["top_secret_action"];
        // echo $post_value;
        thebutton($post_value);
        echo "</div>";
    }

?>