<?php
$doc = new DOMDocument();
$doc->substituteEntities = true;          // この行を追加
$doc->load($_FILES['user']['tmp_name']);
$name = $doc->getElementsByTagName('name')->item(0)->textContent;
$addr = $doc->getElementsByTagName('address')->item(0)->textContent;
?>

<body>
    name: <?php echo htmlspecialchars($name); ?><br>
    bio: <?php echo htmlspecialchars($addr); ?><br>
</body>