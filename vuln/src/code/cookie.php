<?php
setcookie("hoge", "fuga");
setcookie("fuga", 1);
?>

<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<title>cookie</title>
</head>

<body>
	hoge: <?php echo $_COOKIE["hoge"];?><br>
	fuga: <?php echo $_COOKIE["fuga"];?><br>
</body>

</html>