<?php
if($_SERVER['REQUEST_METHOD'] === 'GET'){
?>
<html>
  <head>
    <title>
      Stage 1
    </title>
  </head>
  <body>
    <div style="text-align: center;">
      <form name="Stage1" method="post" action="<?php echo $filename; ?>">
        <h2>Enter your password:</h2>
        <br>
        <input name="password" type="text"><br>
        <br>
        <input type="submit"><br>
        <br>
        <br>
      </form>
    </div>
  </body>
  <!--Don't forget your password is $PASSWORD$--!>
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