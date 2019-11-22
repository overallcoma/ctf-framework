<?php
if($_SERVER['REQUEST_METHOD'] === 'GET'){
?>
<html>
    <head>
        <title>
            Stage 3
        </title>
    </head>
    <body text="#ffffff" bgcolor="#000000">
        <div style="text-align: center;">
            <form name="Stage3" method="post">
                <h2>
                    Enter your password:
                </h2>
                <br>
                <input name="password" type="text">
                <input type="hidden" name="file" value=$PASSWORDPAGE$<br>
                <br>
                <br>
                <input type="submit"><br>
                <br>
                <br>
            </form>
        </div>
    </body>
</html>
<?php
}else {
    $password = $_POST["password"];
    $db = new SQLite3("/db/password.db");
    $result = $db->querySingle("SELECT * FROM passwords WHERE record_number = 1", true);
    $dest_page = "error.html";
    $checkpass = $result["password"];
    if (password_verify($password, $checkpass)) {
        $dest_page = $result["pagename"];
    }
    header("location: $dest_page");
}
?>