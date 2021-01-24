<?php
if (!isset($_COOKIE["name"])) {
	setcookie("name", "yoden");
}
if (!isset($_COOKIE["limit"])) {
	setcookie("limit", 1);
}

try {
	$db = new PDO('mysql:host=db;dbname=docker', 'docker', 'docker');
    $sql = 'SELECT name,pass FROM docker WHERE name=\'' . $_COOKIE["name"] . '\' LIMIT ' . $_COOKIE["limit"] . ';';
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
    <title>cookie based sqli</title>
</head>

<body>
<input type="button" onclick="document.cookie='name=\' or 1=1\%3b--';" value="attack">
    <?
        echo "<p>$sql</p><table border=\"1\"><tr><th>name</th><th>pass</th>";
        foreach( $result as $value ) {
            echo "<tr><td>$value[name] </td><td>$value[pass]</tt></tr>";
	    }
        ?>
    </table>
</body>

</html>