<?php
    $handler = fopen('php://stdin','r') or die($error_message);
    while($stdin_input = fgets($handler,1024));{
    $hashfile = 'hash.txt';
    $handle = fopen($hashfile, 'w') or die('Cannot open file:  '.$hashfile);
    $hashedpassword = password_hash($stdin_input, PASSWORD_DEFAULT);
    fwrite($handle, $hashedpassword);
    fclose($handle);
    $passfile = 'password.txt';
    $handle = fopen($passfile, 'w') or die('Cannot open file: '.$passfile);
    fwrite($handle, $stdin_input);
    fclose($handle);
    }
    die();
?>