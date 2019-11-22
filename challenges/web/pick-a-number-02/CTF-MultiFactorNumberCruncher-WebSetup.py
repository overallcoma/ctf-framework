import random
import string
import subprocess

flag = open('flag.txt', 'r')
flag = flag.read()

form1name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
flagpagename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])

form1name += ".php"
flagpagename += ".php"

secretkey = open('seed.txt', 'r')
secretkey = secretkey.read()

dbfile = "/db/password.db"

indexphp = """<?php
if($_SERVER['REQUEST_METHOD'] === 'GET'){{
?>
<html>
<title>
{0}
</title>
<body>
<form name="checkpage1" method="post" action="<?php echo $filename; ?>">
Pick a number between 000 and 999 <input type="text" name="number1"><br>
<input type="submit">
</form>
</body>
</html>
<?php
}}else {{
  $number = $_POST["number1"];
  $number = (int)$number;  
  $pdo = new PDO("sqlite:/db/password.db");
  $rows = $pdo->query("SELECT * FROM passwords WHERE record_number = 1 AND password = $number");
  $rows = $rows->fetchAll();
  $rowcount = count($rows);
  if($rowcount == 0) {{
    header("location: error.html");
    die();
  }}
  $page = $rows[0]["pagename"];
  header("location: $page");
  die();
}}""".format(secretkey)

form1php = """<?php

$filename = basename(__FILE__);
if($_SERVER['REQUEST_METHOD'] === 'GET'){{
?>
<html>
<title>
{0}
</title>
<body>
<form name="checkpage2" method="post" action="<?php echo $filename; ?>">
Pick a different number between 000 and 999 <input type="text" name="number2"><br>
<input type="submit">
</form>
</body>
</html>
<?php
}}else {{
  $number = $_POST["number2"];
  $number = (int)$number;  
  $pdo = new PDO("sqlite:/db/password.db");
  $rows = $pdo->query("SELECT * FROM passwords WHERE record_number = 2 AND password = $number");
  $rows = $rows->fetchAll();
  $rowcount = count($rows);
  if($rowcount == 0) {{
    header("location: error.html");
    die();
  }}
  $page = $rows[0]["pagename"];
  header("location: $page");
  die();
}}""".format(secretkey)

flagpage = """
<html>
<title>
A Winner is You
</title>
<body>
{0}
</body>
</html>
""".format(flag)

htaccess = """DirectoryIndex index.php
ErrorDocument 404 /error.html
"""

errorpage = """<html>
<title>
Incorrect
</title>
<body>
Gotta be faster to come out on otp of this challenge.
</body>
</html>
"""

file = open('index.php', 'w+')
file.write(indexphp)
file.close()
file = open(form1name, 'w+')
file.write(form1php)
file.close()
file = open(flagpagename, 'w+')
file.write(flagpage)
file.close()
file = open('.htaccess', 'w+')
file.write(htaccess)
file.close()
file = open('error.html', 'w+')
file.write(errorpage)
file.close()


def writeinitialpages(page1_insert, page2_insert):
    file = open('initialpages.txt', 'w+')
    file.write(page1_insert)
    file.write('\n')
    file.write(page2_insert)
    file.close()


writeinitialpages(form1name, flagpagename)
subprocess.run(['httpd', '-D', 'FOREGROUND'])
