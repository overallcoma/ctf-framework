<?php
    $file = 'hash.txt';
    $handle = fopen($file, 'w') or die('Cannot open file:  '.$myfile);
    $hashedpassword = password_hash("$PASSWORD$", PASSWORD_DEFAULT);
    fwrite($handle, $hashedpassword);
    fclose($handle);
    die();
?>