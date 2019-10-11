<?php
$host="db";
$port=3306;
$socket="";
$user="webserver";
$password="webserver";
$dbname="web";

$con = new mysqli($host, $user, $password, $dbname, $port, $socket)
or die ('Could not connect to the database server' . mysqli_connect_error());

$sql = "SELECT * FROM hackers";
$result = $con->query($sql);
$hackerinfo = $result->fetch_assoc();
$con->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Skull*Sec</title>
</head>
<body text="#ffffff" bgcolor="#000000" link="blue">

<?php
foreach($hackerinfo as $single_hacker)
    {
        $avataer_file = $single_hacker["avatar"];
        $hacker_avatar = "/images/".$avataer_file;
        $hacker_handle = $single_hacker["handle"];
        $hacker_about = $single_hacker["abouut"];
        ?>
        <table align="center" border="0" cellspacing="0" cellpadding="0">
            <tr>
                <td>
                    <img src="<?php echo $hacker_avatar ?>">
                </td>
                <td width="5">
                </td>
                <td valign="top">
                    <h2><?php echo $hacker_handle ?></h2>
                    <br>
                    <?php echo $hacker_about ?>
                </td>
            </tr>
        </table>
        <br>
    <?php } ?>
<table align="center" border="0" cellpadding="40" cellpadding="0">
    <td><a href="aboutus.html">About Us</a></td><td><a href="ourhacks.html">Our Hacks</a></td><td><a href="ourhackers.html">Our Hackers</a></td>
</table>
</body>
</html>
