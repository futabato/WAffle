<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>xxe</title>
</head>

<body>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="user" />
        <input type="submit" />
    </form>
    <hr>
    <?php
    $doc = new DOMDocument();
    $doc->substituteEntities = true;          // この行を追加
    if (isset($_FILES['user']['tmp_name'])) {
        $doc->load($_FILES['user']['tmp_name']);
        $name = $doc->getElementsByTagName('name')->item(0)->textContent;
        $addr = $doc->getElementsByTagName('bio')->item(0)->textContent;

        echo 'name: ' . htmlspecialchars($name) . '<br>';
        echo 'bio: ' . htmlspecialchars($addr);
    }

    ?>
</body>

</html>