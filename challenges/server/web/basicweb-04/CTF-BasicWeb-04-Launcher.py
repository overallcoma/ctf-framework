import sqlite3
import random
import string
import subprocess
import os


def dbconnect(dbfile_func):
    try:
        connection = sqlite3.connect(dbfile_func)
        print(sqlite3.version)
        connection.close()
    except sqlite3.Error as t:
        print(t)
        exit(1)


def write_database(dbfile_func, insert_password, insert_page):
    try:
        connection = sqlite3.connect(dbfile_func, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        droptablestatement = "DROP TABLE IF EXISTS passwords"
        cursor.execute(droptablestatement)
        cursor.close()
        connection.close()
        connection = sqlite3.connect(dbfile_func, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        createtablestatement = 'CREATE TABLE IF NOT EXISTS passwords (record_number integer PRIMARY KEY AUTOINCREMENT, password text, pagename text)'
        cursor.execute(createtablestatement)
        connection.commit()
        cursor.close()
        connection.close()
        connection = sqlite3.connect(dbfile_func, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO passwords VALUES (NULL, ?, ?)", (insert_password, insert_page))
        connection.commit()
        cursor.close()
        connection.close()
    except sqlite3.Error as t:
        print(t)


def generate_pass_hash(password):
    passwordgenphp = """<?php
    $file = 'hash.txt';
    $handle = fopen($file, 'w') or die('Cannot open file:  '.$myfile);
    $hashedpassword = password_hash("{0}", PASSWORD_DEFAULT);
    fwrite($handle, $hashedpassword);
    fclose($handle);
    die();
    ?>""".format(password)
    file = open('hashgen.php', 'w+')
    file.write(passwordgenphp)
    file.close()
    subprocess.call(["php", "hashgen.php"])
    file = open('hash.txt', 'r')
    hashed_password = file.read()
    file.close()
    os.remove("hash.txt")
    os.remove("hashgen.php")
    return hashed_password


flag = os.environ['FLAG']
password = os.environ['PASSWORD']

flagpagename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
flagpagename += ".php"

dbfile = "/db/password.db"

hashed_password = password

write_database(dbfile, hashed_password, flagpagename)

indexphp = """<?php
if($_SERVER['REQUEST_METHOD'] === 'GET'){{
?>
<html>
  <head>
    <title>
      Stage 4
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
        </form>
        <br>
        <form action="sendpass.php" method="post">
        <input type="hidden" name="to" value="berkmikely@h4110w33n.com">
        <input type="submit" value="Send Password Reminder">
        </form>        
        <br>
    </div>
  </body>
</html>
<?php
}}else {{
  $password = $_POST["password"];
  $hashedpassword = password_hash($password, PASSWORD_DEFAULT);
  $pdo = new PDO("sqlite:/db/password.db");
  $sql_return = $pdo->query("SELECT * FROM passwords WHERE record_number = 1");
  $sql_return = $sql_return->fetch();
  if ($password != $sql_return["password"]){{
    header("location: error.html");
    die();
  }}
  $page = $sql_return["pagename"];
  header("location: $page");
}}
?>""".format(password)

sendpassphp = """
<?php
if($_SERVER['REQUEST_METHOD'] === 'POST'){{
  $email_target = $_POST["to"];  
  $pdo = new PDO("sqlite:/db/password.db");
  $sql_return = $pdo->query("SELECT * FROM passwords WHERE record_number = 1");
  $sql_return = $sql_return->fetch();
  $password = $sql_return["password"];
  $msg = "As a reminder - your password is $password\nStay Spooky!";
  $subject = "Your Password Reset";
  $headers = "From: DO_NOT_REPLY@h4110w33n.com";
  mail($email_target,$subject,$msg,$headers);
  $dest_page = "resetsuccess.html";
  header("location: $dest_page");
  die();
}}else{{
?>
<html>
  <head>
    <title>
      Stage 4
    </title>
  </head>
  <body>
    <div style="text-align: center;">
    <h2>Here thar be dragons</h2>
    </div>     
  </body>
</html>
<?php
}}
?>
"""

resetsuccesshtml = """
<html>
  <head>
    <title>
      Stage 4
    </title>
  </head>
  <body>
    <div style="text-align: center;">
      <h2>Password Reminder Sent</h2>      
    </div>
  </body>
</html>
"""

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
Try Again!
</body>
</html>
"""

file = open('index.php', 'w+')
file.write(indexphp)
file.close()
file = open(flagpagename, 'w+')
file.write(flagpage)
file.close()
file = open('sendpass.php', 'w+')
file.write(sendpassphp)
file.close()
file = open('resetsuccess.html', 'w+')
file.write(resetsuccesshtml)
file.close()
file = open('.htaccess', 'w+')
file.write(htaccess)
file.close()
file = open('error.html', 'w+')
file.write(errorpage)
file.close()

subprocess.call(['httpd', '-D', 'FOREGROUND'])
