<?php
$cookie_name = "Seceret";
$cookie_value = "Datrac";
setcookie($cookie_name, $cookie_value, time() + (86400 *30), "/");
?>
<html>
<body>

<?php
if(!isset($_COOKIE[$cookie_name])) {
} else {
	echo "Cookie '".$cookie_name."'is set!<br>";
	echo "Value is; ".$_COOKIE[$cookie_name];
}
?>

</body>
</html>
