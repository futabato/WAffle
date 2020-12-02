<?php
$cookie_name = "hoge";
$cookie_value = "huga";
setcookie($cookie_name, $cookie_value);
?>

<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<title>cookie</title>
</head>

<body>

<?php
if(!isset($_COOKIE[$cookie_name])) {
} else {
	echo "Cookie name '".$cookie_name."'<br>";
	echo "value: ".$_COOKIE[$cookie_name];
}
?>

</body>
</html>
