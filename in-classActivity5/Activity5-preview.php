<?php
echo "<h1>Preview</h1>";
if(empty($_GET['name']) == false) {
        echo $_GET['name'] . "<br>";
    }
    else {
        echo "Name is empty" . "<br>";
    }

    if(empty($_GET['username']) == false) {
        echo $_GET['username'] . "<br>";
    }
    else {
        echo "Username is empty" . "<br>";
    }

    if(empty($_GET['password']) == false) {
        echo $_GET['password'] . "<br>";
    }
    else {
        echo "Password is empty" . "<br>";
    }

    if(empty($_GET['adress']) == false) {
        echo $_GET['adress'] . "<br>";
    }
    else {
        echo "Adress is empty" . "<br>";
    }

    if(empty($_GET['country']) == false) {
        echo $_GET['country'] . "<br>";
    }
    else {
        echo "Country is empty" . "<br>";
    }

    if(empty($_GET['zip']) == false) {
        echo $_GET['zip'] . "<br>";
    }
    else {
        echo "Zip Code is empty" . "<br>";
    }

    if(empty($_GET['email']) == false) {
        echo $_GET['email'] . "<br>";
    }
    else {
        echo "Email is empty" . "<br>";
    }

    if(empty($_GET['sex']) == false) {
        echo $_GET['sex'] . "<br>";
    }
    else {
        echo "Sex is empty" . "<br>";
    }

    if(isset($_GET['language']) && is_array($_GET['language']) && count($_GET['language']) > 0) {
        foreach($_GET['language'] as $language) {
            echo $language . "<br>";
        }
    } else {
        echo "Language is empty" . "<br>";
    }
    

    if(empty($_GET['about']) == false) {
        echo $_GET['about'] . "<br>";
    }
    else {
        echo "About is empty" . "<br>";
    }

?>