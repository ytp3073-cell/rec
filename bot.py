<?php
$BOT_TOKEN = "8513005164:AAHSB3MEuhcWAZSESON3gc8JfIYgY_dCDIk";
$API = "https://api.telegram.org/bot$BOT_TOKEN";

$update = json_decode(file_get_contents("php://input"), true);

if (!isset($update["channel_post"])) {
    exit;
}

$chat_id = $update["channel_post"]["chat"]["id"];
$message_id = $update["channel_post"]["message_id"];

// 👉 yahi tumhara reaction url
$reaction_url = "https://reaction.xo.je/reaction.php?chat_id=$chat_id&msg_id=$message_id";

// call reaction api
file_get_contents($reaction_url);
?>
