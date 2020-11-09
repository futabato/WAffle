<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>

<body>
    <ul>
        <li>
            <a href="?msg=hello">hello</a>
        </li>
        <li>
            <a href="?msg=bye-bye">bye</a>
        </li>
        <li>
            <a href="?msg=;ls">ls</a>
        </li>
    </ul>
    <hr>
    <?php
    if (isset($_GET['msg'])) {
        exec("echo " . $_GET['msg'], $output);
        echo "<pre>";
        print_r($output);
        echo "</pre>";
    }
    ?>
</body>

</html>