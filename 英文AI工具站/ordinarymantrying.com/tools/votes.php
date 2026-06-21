<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Cache-Control: no-store');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

$DATA_FILE = __DIR__ . '/votes_data.json';
$LOG_FILE  = __DIR__ . '/votes_log.json';

function load_arr($file) {
    if (!file_exists($file)) return [];
    $raw = file_get_contents($file);
    if (!$raw) return [];
    $d = json_decode($raw, true);
    return is_array($d) ? $d : [];
}

function save_arr($file, $arr) {
    file_put_contents($file, json_encode($arr, JSON_FORCE_OBJECT));
}

// ── GET ──────────────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $data = load_arr($DATA_FILE);
    echo json_encode($data, JSON_FORCE_OBJECT);
    exit;
}

// ── POST ─────────────────────────────────────────────────────────
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $raw  = file_get_contents('php://input');
    $body = json_decode($raw, true);
    $code = isset($body['code']) ? preg_replace('/[^A-Za-z0-9]/', '', (string)$body['code']) : '';

    if (!$code) {
        http_response_code(400);
        echo json_encode(['error' => 'missing code']);
        exit;
    }

    // Rate limit: 1 vote per IP+code per 24h
    $ip  = md5(isset($_SERVER['HTTP_X_FORWARDED_FOR'])
        ? explode(',', $_SERVER['HTTP_X_FORWARDED_FOR'])[0]
        : $_SERVER['REMOTE_ADDR']);
    $key = $ip . '_' . $code;
    $log = load_arr($LOG_FILE);
    $now = time();

    if (isset($log[$key]) && ($now - $log[$key]) < 86400) {
        echo json_encode(['ok' => false, 'reason' => 'already_voted']);
        exit;
    }

    // Increment
    $data         = load_arr($DATA_FILE);
    $data[$code]  = (isset($data[$code]) ? (int)$data[$code] : 0) + 1;
    save_arr($DATA_FILE, $data);

    // Log + prune
    $log[$key] = $now;
    foreach ($log as $k => $t) {
        if ($now - $t > 172800) unset($log[$k]);
    }
    save_arr($LOG_FILE, $log);

    echo json_encode(['ok' => true, 'total' => $data[$code]]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'method not allowed']);
