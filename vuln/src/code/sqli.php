<?php
try {
    $db = new PDO('mysql:host=db;dbname=docker', 'docker', 'docker');
    $sql = 'SELECT name,pass FROM docker WHERE name=\'' . $_GET["input"] . '\';';
    $stmt = $db->prepare($sql);
    $stmt->execute();
    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    echo $e->getMessage();
    exit;
} ?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>post</title>
</head>

<body>
    <form method="GET">
        name <input type="text" name="input" size="50" id="input"><br>
        <input type="button" onclick="document.getElementById('input').value = '\'or 1=1\;--';" value="attack"><input type="submit" value="送信">
    </form>
    <hr>
    <?
        echo "<p>$sql</p><table border=\"1\"><tr><th>name</th><th>pass</th>";
        foreach( $result as $value ) {
            echo "<tr><td>$value[name] </td><td>$value[pass]</tt></tr>";
	    }
        ?>
    </table>
</body>

</html>