<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>

<body>
    <ul>
        <li>
            <a href="?input=index.php">index</a>
        </li>
        <li>
            <a href="?input=php://filter/convert.base64-encode/resource=index.php">base64(index)</a>
        </li>
    </ul>
    <hr>
    <?php
    if (isset($_GET['input'])) {
        $file = $_GET['input'];
        include($file);
    }
    ?>
</body>

</html>