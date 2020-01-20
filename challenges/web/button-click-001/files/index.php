<?php
    session_start();
    if (!isset($_POST['click'])) {
        $_SESSION['totalclicks'] = 1;
    }
?>
<html>
    <head>
        <title>
            Button-Clicker-001
        </title>
    </head>
    <body text="#ffffff" bgcolor="#000000">
        <div style="text-align: center;">
            <form name="ButtonClicker-001" method="post">
                <h2>
                    Click the button 500 times!
                </h2>
                <br>
                <h3>
                Total Button Presses: <?php echo $_SESSION['clicks']++ ?>
                <br>
                <input type="submit" name="click" value="The Button"/>
                <br>
                <br>
            </form>
        </div>
    </body>
</html>