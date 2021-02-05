<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>get</title>
</head>

<body>
    <form action="" method="get">
        <input type="text" name="input" size="50" id="input"><br>
        <input type="button" onclick="document.getElementById('input').value = '<script>alert(1)</script>';" value="attack"><input type="submit" value="送信">
    </form>
    <hr>
    output: <?php
            $input = $_GET["input"];
            print $input;
            ?>
</body>

</html>