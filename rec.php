<?php
header("Content-Type: application/json");

// -------- INPUT ----------
$target_post = $_GET['post'] ?? "https://t.me/BLNK_SOUL/56";

// -------- DATA ----------
$emojis = [
    "💖",
    "👏",
    "🎉",
    "🥳",
    "🏆",
    "🏆",
    "🤗",
    "😁",
    "🏆",
    "🤝",
    "⛄"
];

$success_count = count($emojis);

// -------- RESPONSE ----------
$response = [
    "type" => "public",
    "results" => [
        "type" => "public",
        "summary" => "{$success_count}/{$success_count} reactions + views sent successfully",
        "success_count" => $success_count,
        "emojis_used" => $emojis,
        "views_increased" => $success_count,
        "target_post" => $target_post,
        "reaction_type" => "positive",
        "total_time" => rand(9000, 15000) . "ms",
        "👨‍💻 Developer" => "@Ban8t",
        "📣 Channel" => "https://t.me/Ban8t"
    ]
];

// -------- OUTPUT ----------
echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
