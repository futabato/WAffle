<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<title>receive</title>
</head>

<body>
	<p>GET:
		<?php
		$input3 = $_GET["input"];
		print $input3;
		?>
	</p>
	<p>POST:
		<?php
		$input = $_POST["input"];
		$input2 = $_POST["input2"];
		print $input . "," . $input2;
		?>
	</p>
</body>

</html>