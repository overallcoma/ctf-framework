<?php
    $inputfile_content = file_get_contents("/var/www/html/password.txt");
    $inputfile_content =  preg_replace('/\s+/', '', $inputfile_content);
    $outputfile = 'hash.txt';
    $handle = fopen($outputfile, 'w') or die('Cannot open file: '.$outputfile);
    $hashedpassword = password_hash($inputfile_content, PASSWORD_DEFAULT);
    fwrite($handle, $hashedpassword);
    fclose($handle);
    die();
?>