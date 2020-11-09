<?php
try {
    $db = new PDO('mysql:host=db;dbname=docker', 'docker', 'docker');
    $sql = 'SELECT name,pass FROM docker WHERE name=\''.$_GET["name"].'\';';
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
    <title>sql</title>
</head>

<body>
    <ul>
    <?
    echo "<p>$sql</p><table border=\"1\"><tr><th>name</th><th>pass</th>";
    foreach( $result as $value ) {
        echo "<tr><td>$value[name] </td><td>$value[pass]</tt></tr>";
	}
    ?>
    </table>
    </ul>
</body>

</html>