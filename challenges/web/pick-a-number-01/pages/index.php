<?php
if($_SERVER['REQUEST_METHOD'] === 'GET'){
?>

<html>
    <title>
        Pick A Number
    </title>
    <body text="#ffffff" bgcolor="#000000" link="blue">
        <div style="text-align: center;">
            <form name="magicnumber" method="post" action=">
                <h2> Pick a number between 0 and 10,000 </h2>
                <input type="text" name="number">
                <br>
                <input type="submit">
            </form>
        </div>
    </body>
</html>

<?php
}else {
  $number = $_POST["magicnumber"];
  $targetpage = number . ".html"
  header("location: $number");
?>