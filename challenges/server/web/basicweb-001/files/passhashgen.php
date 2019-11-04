<?php
    $inputfile = file_get_contents("/var/www/html/password.txt");
    $outputfile = "hash.txt";
    $handle = fopen($file, 'w') or die('Cannot open file:  '.$outputfile);
    $hashedpassword = password_hash($stdin_input, PASSWORD_DEFAULT);
    fwrite($handle, $hashedpassword);
    fclose($handle);
    }
    die();
?>