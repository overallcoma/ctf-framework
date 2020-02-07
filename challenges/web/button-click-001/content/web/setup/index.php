<?php
    session_start();
?>
<html>
    <head>
        <title>
            ButtonClicker!
        </title>
    </head>
    <body text="#ffffff" bgcolor="#000000">
        <div style="text-align: center;">
            <h2>
                CLICK THE BUTTON UNCONFIGURED_CLICK_COUNT TIMES!!!
            </h2>
            <form method="post">
                <input type="hidden" name="top_secret_action" id="top_secret_action" value="<?php echo session_id(); ?>" >
                <img src="/images/arrow1.png" style="width:40px;height:40px;">
                <input type="submit" name="thebutton" class="button" value="Click The Button!" >
                <img src="/images/arrow2.png" style="width:40px;height:40px;">
            </form>
    		<br>
	    	<br>
	    	<h4>
	    	    Your click count is -
	    	    <?php
	    	    function thebutton($post_value) {
                    $servername = "db";
                    $username = "buttonclick";
                    $password = "buttonclick";
                    $dbname = "buttonclickerdb";
                    $session_id = session_id();
                    $conn = new mysqli($servername, $username, $password, $dbname);
                    $session_add_click = "UPDATE buttonclicker_table SET click_count = click_count + 1 WHERE session_key = '$post_value';";
                    $result = $conn->query($session_add_click);
                    $conn->close();
                    $conn = new mysqli($servername, $username, $password, $dbname);
                    $session_clickcount_query = "SELECT click_count FROM buttonclicker_table WHERE session_key = '$post_value' LIMIT 1;";
                    $result = $conn->query($session_clickcount_query);
                    while ($row = $result->fetch_assoc()) {
                        return $row["click_count"];
                    }
                }
                    if(isset($_REQUEST['thebutton'])) {
                        $post_value = $_POST["top_secret_action"];
                        $click_count_current = thebutton($post_value);
                        echo $click_count_current;
                    }

                    else {
                            $servername = "db";
                            $username = "buttonclick";
                            $password = "buttonclick";
                            $dbname = "buttonclickerdb";
                            $session_id = session_id();
                            $conn = new mysqli($servername, $username, $password, $dbname);
                            $create_record_query = "INSERT INTO buttonclicker_table (session_key, click_count) VALUES ('$session_id',0);";
                            $conn->query($create_record_query);
                            $conn->close();
                        echo "???";
                    }
                ?>
        <?php
            if ($click_count_current >= 140) {
                echo "<br>";
                echo "<h1>";
                echo "YAY!";
                echo "</h1>";
                echo "<h2>";
                $flag_value = "UNCONFIGURED_FLAG_VALUE";
                echo $flag_value;
                echo "</h2>";
            }
        ?>
        </div>
    </body>
</html>