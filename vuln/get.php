<?php

if (isset($_GET["input"])) {
    $string = $_GET["input"];
    echo $string;
} else {
    highlight_file(__FILE__);
}
