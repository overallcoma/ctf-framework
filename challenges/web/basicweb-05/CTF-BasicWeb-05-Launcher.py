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


def get_ciphered_password(password):
    output_string = ''
    round_count = 0
    for character in password:
        cipher_char = ord(character)
        cipher_char = cipher_char + round_count
        cipher_char = chr(cipher_char)
        output_string += cipher_char
        round_count = round_count + 1
    return output_string


flag = os.environ['FLAG']
password = os.environ['PASSWORD']
ciphered_password = get_ciphered_password(password)

flagpagename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(64)])
flagpagename += ".php"

dbfile = "/db/password.db"

write_database(dbfile, password, flagpagename)

indexphp = """<?php
if($_SERVER['REQUEST_METHOD'] === 'GET'){{
?>
<html>
  <head>
    <title>
      Stage 6
    </title>
  </head>
  <body>
    <div style="text-align: center;">
        <form action="cipherstring.php" method="post">
        <br>
        <h2> Enter a string to encrypt here: </h2>
        <br>
        <input name="string" type="text">
        <br>
        <input type="submit">
        </form>
        <br>
        <br>
        <h3>You recovered the password hash of {0}</h3>
        <br>
        <br>
        <form name="Stage6" method="post">
        <h2> Enter your password: </h2>
        <br>
        <input name="password" type="text">
        <br>
        <input type="submit"><br>
        <br>
        <br>
      </form>
    </div>
  </body>
</html>
<?php
}}else {{
  $password = $_POST["password"];
  $pdo = new PDO("sqlite:/db/password.db");
  $sql_return = $pdo->query("SELECT * FROM passwords WHERE record_number = 1");
  $sql_return = $sql_return->fetch();
  $dest_page = "error.html";
  if($sql_return["password"] == $password){{
    $dest_page = $sql_return["pagename"];
    }}
  header("location: $dest_page");
}}
?>""".format(ciphered_password)

cipherstringphp = """
<?php
if($_SERVER['REQUEST_METHOD'] === 'POST'){{
  $submitted_string = $_POST["string"];
  $ciphered_string = " ";
  $counter = 0;
  $string_split = str_split($submitted_string);
  foreach($string_split as $character){{
    $character_ord = ord($character);
    $character_ord = ($character_ord + $counter);
    $character_ascii = chr("$character_ord");
    $cipher_string = ($cipher_string . $character_ascii);
    $counter++;
    }}
    ?>
      <html>
        <head>
          <title>
            Ciphered String
          </title>
       </head>
       <body>
       <div style="text-align: center;">
        <br>
        <hd> Your ciphered string is <?php echo $cipher_string; ?> </h2>
        <br>
    </div>
  </body>
</html>
<?php 
}}else{{
?>
<html>
  <head>
    <title>
      Go Away
    </title>
  </head>
  <body>
    <div style="text-align: center;">
        <h2>That's not how the game is played.</h2>
    </div>
  </body>
</html>
<?php
}}
?>"""

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
file = open('cipherstring.php', 'w+')
file.write(cipherstringphp)
file.close()
file = open('.htaccess', 'w+')
file.write(htaccess)
file.close()
file = open('error.html', 'w+')
file.write(errorpage)
file.close()

subprocess.call(['httpd', '-D', 'FOREGROUND'])
