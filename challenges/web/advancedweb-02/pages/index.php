<?php
if($_SERVER['REQUEST_METHOD'] === 'GET'){
?>
<html>
  <head>
    <title>
      Awesome Server Ping Checker
    </title>
  </head>
  <body text="#ffffff" bgcolor="#000000" link="blue">
    <div style="text-align: center;">
      <form name="checkpage1" method="post">
        <h2>Enter an IP address to check!</h2>
        <br>
        <input name="ip" type="text"><br>
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
$ip = $_POST["ip"];
$strings = explode (" ", $ip);
$corrected_ip = $strings[0];
$additional_input = array_splice($strings, 1);
$additional_input = implode(" ", $additional_input);
$cmd = "ping $corrected_ip -c 5 $additional_input";
$output = shell_exec($cmd);
?>
<html>
  <head>
    <title>
      Awesome Server Ping Checker
    </title>
  </head>
  <body text="#ffffff" bgcolor="#000000" link="blue">
    <div style="text-align: center;">
      <form name="checkpage1" method="post">
        <h2>Enter an IP address to check!</h2>
        <br>
        <input name="ip" type="text"><br>
        <br>
        <input type="submit"><br>
        <br>
        <br>
        <div style="text-align: left;">
        <?php
            echo "<pre>$output</pre>";
        ?>
        </div>
        </form>
    </div>
  </body>
</html>
<?php
}
?>