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
  <head>
    <title>
      {0}
    </title>
  </head>
  <body>
    <div style="text-align: center;">
      <form name="checkpage1" method="post" action="&lt;?php echo $filename; ?&gt;">
        <h2>
          Pick a number between 000 and 999</h2>
        <br>
        &nbsp;<input name="number1" type="text"><br>
        <br>
        <input type="submit"><br>
        <br>
        <br>
        <h3>
          --- The Time Is !!!NO TIME PRESENT!!! UTC --- </h3>
        <h1>
        </h1>
      </form>
    </div>
  </body>
<!-- Thanks, simonseo and kislyuk, for this wonderful Python Module --!>
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
if($_SERVER['REQUEST_METHOD'] === 'GET'){{
?>
<html>
  <head>
    <title>
      {0}
    </title>
  </head>
  <body>
    <div style="text-align: center;">
      <form name="checkpage1" method="post" action="&lt;?php echo $filename; ?&gt;">
        <h2>
          Pick a number between 000 and 999</h2>
        <br>
        &nbsp;<input name="number1" type="text"><br>
        <br>
        <input type="submit"><br>
        <br>
        <br>
        <h3>
          --- The Time Is !!!NO TIME PRESENT!!! UTC --- </h3>
        <h1>
        </h1>
      </form>
    </div>
    query("SELECT * FROM passwords WHERE record_number = 1 AND password =
    $number"); $rows = $rows-&gt;fetchAll(); $rowcount = count($rows);
    if($rowcount == 0) {{ header("location: error.html"); die(); }} $page =
    $rows[0]["pagename"]; header("location: $page"); die();
    }}
  </body>
<!-- Thanks, simonseo and kislyuk, for this wonderful Python Module --!>
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
# subprocess.run(['httpd', '-D', 'FOREGROUND'])
