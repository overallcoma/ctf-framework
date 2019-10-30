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
  $hashedpassword = password_hash($password, PASSWORD_DEFAULT);
  $pdo = new PDO("sqlite:/db/password.db");
  $sql_return = $pdo->query("SELECT * FROM passwords WHERE record_number = 1");
  $sql_return = $sql_return->fetch();
  $goodorbad = password_verify($password, $sql_return["password"]);
  $dest_page = "error.html";
  if($goodorbad){
    $dest_page = $sql_return["pagename"];
  }
  header("location: $dest_page");
}
?>