import sqlite3
import random
import string
import subprocess
import os


# def dbconnect(dbfile_func):
#     try:
#         connection = sqlite3.connect(dbfile_func)
#         print(sqlite3.version)
#         connection.close()
#     except sqlite3.Error as t:
#         print(t)
#         exit(1)


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
        createtablestatement = 'CREATE TABLE [IF NOT EXISTS passwords (record_number integer PRIMARY KEY AUTOINCREMENT, password text, pagename text)'
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

hashed_password = generate_pass_hash(password)

write_database(dbfile, hashed_password, flagpagename)

indexphp = """<?php
if($_SERVER['REQUEST_METHOD'] === 'GET'){{
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
  <!--Don't forget your password is {0}--!>
</html>
<?php
}}else {{
  $password = $_POST["password"];
  $hashedpassword = password_hash($password, PASSWORD_DEFAULT);
  $pdo = new PDO("sqlite:/db/password.db");
  $sql_return = $pdo->query("SELECT * FROM passwords WHERE record_number = 1");
  $sql_return = $sql_return->fetch();
  $goodorbad = password_verify($password, $sql_return["password"]);
  $dest_page = "error.html";
  if($goodorbad){{
    $dest_page = $sql_return["pagename"];
  }}
  header("location: $dest_page");
}}
?>""".format(password)

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
file = open('.htaccess', 'w+')
file.write(htaccess)
file.close()
file = open('error.html', 'w+')
file.write(errorpage)
file.close()

subprocess.call(['httpd', '-D', 'FOREGROUND'])
