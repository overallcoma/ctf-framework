<?php
    $handler = fopen('php://stdin','r') or die($error_message);
    while($stdin_input = fgets($handler,1024));{
    $file = 'hash.txt';
    $handle = fopen($file, 'w') or die('Cannot open file:  '.$file);
    $hashedpassword = password_hash($stdin_input, PASSWORD_DEFAULT);
    fwrite($handle, $hashedpassword);
    fclose($handle);
    }
    die();
?>