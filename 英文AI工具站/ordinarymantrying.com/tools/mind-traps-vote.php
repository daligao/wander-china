<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit(0); }

$file = __DIR__ . '/mind-traps-votes.json';

$valid = [
    "Murphy's Law","Pareto Principle","Butterfly Effect","Matthew Effect",
    "Halo Effect","Bystander Effect","Hawthorne Effect","Pygmalion Effect",
    "Barnum Effect","Parkinson's Law","10,000-Hour Rule","Herd Mentality",
    "Ratchet Effect","Primacy Effect","Recency Effect","Domino Effect",
    "Analysis Paralysis","Birdcage Effect","Catfish Effect","Kuleshov Effect",
    "Anchoring Effect","Authority Bias","Dunning-Kruger Effect","Sunk Cost Fallacy",
    "Streisand Effect","Weakest Link","Segal's Law","Door-in-the-Face Technique",
    "Tunnel Vision Effect","Gadfly Effect","Blind Following Effect","Peak-End Rule",
    "Survivorship Bias","Confirmation Bias","Gambler's Fallacy","IKEA Effect",
    "Spotlight Effect","Cobra Effect","Ben Franklin Effect","Goodhart's Law"
];

function getTop8($votes) {
    arsort($votes);
    $top = array_slice($votes, 0, 8, true);
    $result = [];
    foreach ($top as $law => $count) {
        $result[] = ['law' => $law, 'votes' => (int)$count];
    }
    return $result;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);
    $law = isset($data['law']) ? trim($data['law']) : '';

    if (!in_array($law, $valid, true)) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid law']);
        exit;
    }

    $fp = fopen($file, 'c+');
    if (!$fp || !flock($fp, LOCK_EX)) {
        http_response_code(500);
        echo json_encode(['error' => 'Lock failed']);
        if ($fp) fclose($fp);
        exit;
    }

    $size = filesize($file);
    $votes = $size > 0 ? json_decode(fread($fp, $size), true) : [];
    if (!is_array($votes)) $votes = [];

    $votes[$law] = ($votes[$law] ?? 0) + 1;

    rewind($fp);
    $json = json_encode($votes, JSON_PRETTY_PRINT);
    fwrite($fp, $json);
    ftruncate($fp, strlen($json));
    flock($fp, LOCK_UN);
    fclose($fp);

    echo json_encode([
        'success' => true,
        'voted'   => $law,
        'count'   => $votes[$law],
        'top8'    => getTop8($votes)
    ]);

} else {
    if (!file_exists($file)) { echo json_encode([]); exit; }
    $votes = json_decode(file_get_contents($file), true);
    if (!is_array($votes)) { echo json_encode([]); exit; }
    echo json_encode(getTop8($votes));
}
