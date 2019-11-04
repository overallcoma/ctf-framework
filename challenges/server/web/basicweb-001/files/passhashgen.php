<?php
    $inputfile_content = file_get_contents("/var/www/html/password.txt")
    // $handler = fopen('php://stdin','r') or die($error_message);
    //while($stdin_input = fgets($handler,1024));{
    $outputfile = 'hash.txt';
    $handle = fopen($outputfile, 'w') or die('Cannot open file: '.$outputfile);
    $hashedpassword = password_hash($inputfile_content, PASSWORD_DEFAULT);
    fwrite($handle, $hashedpassword);
    fclose($handle);
    //}
    die();
?>