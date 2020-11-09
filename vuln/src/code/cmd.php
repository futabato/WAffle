<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>

<body>
    <ul>
        <li>
            <a href="?input=hello">hello</a>
        </li>
        <li>
            <a href="?input=bye-bye">bye</a>
        </li>
        <li>
            <a href="?input=;ls">ls</a>
        </li>
    </ul>
    <hr>
    <?php
    if (isset($_GET['input'])) {
        exec("echo " . $_GET['input'], $output);
        echo "<pre>";
        print_r($output);
        echo "</pre>";
    }
    ?>
</body>

</html>