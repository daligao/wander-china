<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit; }

$file = __DIR__ . '/standup-scores.json';
$lock = __DIR__ . '/standup-scores.lock';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $raw   = json_decode(file_get_contents('php://input'), true) ?? [];
    $name  = substr(strip_tags(trim($raw['name'] ?? '')), 0, 20);
    if (!$name) $name = 'Anonymous';
    $peak  = max(0, round((float)($raw['peak']   ?? 0), 2));
    $allowed_occ = ['Software Developer','Data Analyst','UI/UX Designer','Content Writer',
                    'Digital Marketer','Product Manager','Accountant','Customer Support',
                    'Project Manager','Video Editor','System Admin','Trader/Investor',
                    'Sales','HR','Student','Freelancer','Other'];
    $occ   = in_array($raw['occ'] ?? '', $allowed_occ) ? $raw['occ'] : 'Other';
    $entry = [
        'name'   => $name,
        'occ'    => $occ,
        'peak'   => $peak,
        'breaks' => max(0, (int)($raw['breaks'] ?? 0)),
        'mins'   => max(0, (int)($raw['mins']   ?? 0)),
        'cause'  => in_array($raw['cause'] ?? '', ['overload','drain']) ? $raw['cause'] : 'drain',
        'ts'     => time(),
    ];

    $lk = fopen($lock, 'c');
    flock($lk, LOCK_EX);
    $scores = file_exists($file) ? (json_decode(file_get_contents($file), true) ?? []) : [];
    $scores[] = $entry;
    usort($scores, fn($a,$b) => $b['peak'] <=> $a['peak']);
    $scores = array_slice($scores, 0, 500);
    file_put_contents($file, json_encode($scores));
    flock($lk, LOCK_UN);
    fclose($lk);

    $rank = 0;
    foreach ($scores as $i => $s) {
        if ($s['name']===$entry['name'] && $s['peak']===$entry['peak'] && $s['ts']===$entry['ts']) {
            $rank = $i + 1; break;
        }
    }
    echo json_encode(['ok'=>true, 'rank'=>$rank, 'total'=>count($scores)]);

} else {
    $scores = file_exists($file) ? (json_decode(file_get_contents($file), true) ?? []) : [];
    usort($scores, fn($a,$b) => $b['peak'] <=> $a['peak']);
    echo json_encode(array_slice($scores, 0, 20));
}
