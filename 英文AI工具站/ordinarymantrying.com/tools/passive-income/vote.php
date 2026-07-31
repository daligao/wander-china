<?php
define('DATA_FILE', __DIR__ . '/passive-income-votes.json');
define('SIMPLEVOTES_FILE', __DIR__ . '/passive-income-simplevotes.json');
define('ADMIN_KEY', 'pi2026admin');

function loadSimpleVotes() {
    if (!file_exists(SIMPLEVOTES_FILE)) return [];
    return json_decode(file_get_contents(SIMPLEVOTES_FILE), true) ?: [];
}
function saveSimpleVotes($d) {
    return file_put_contents(SIMPLEVOTES_FILE, json_encode($d, JSON_PRETTY_PRINT), LOCK_EX);
}
function getScores($votes) {
    $scores = [];
    foreach ($votes as $v) {
        $sid = $v['stream_id'];
        if (!isset($scores[$sid])) $scores[$sid] = ['up' => 0, 'down' => 0];
        $scores[$sid][$v['vote']]++;
    }
    return $scores;
}

header('Content-Type: application/json');
header('Cache-Control: no-store, no-cache, must-revalidate');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

function loadData() {
    if (!file_exists(DATA_FILE)) return [];
    return json_decode(file_get_contents(DATA_FILE), true) ?: [];
}
function saveData($d) {
    return file_put_contents(DATA_FILE, json_encode($d, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
}
function hashIp($ip) {
    return hash('sha256', $ip . 'pi_salt_ord2026');
}
function containsUrl($text) {
    return preg_match('/https?:\/\/|www\.|\.com|\.net|\.org|\.io|\.xyz|\.info|\.co\b/i', $text);
}

$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? '';
$key    = $_GET['key'] ?? '';

// ── GET: vote scores (public) ────────────────────────────────────────────────
if ($method === 'GET' && $action === 'scores') {
    echo json_encode(['ok' => true, 'scores' => getScores(loadSimpleVotes())]);
    exit;
}

// ── POST: simple up/down vote (public) ───────────────────────────────────────
if ($method === 'POST' && $action === 'vote') {
    $body      = json_decode(file_get_contents('php://input'), true);
    $stream_id = (int)($body['stream_id'] ?? 0);
    $vote      = $body['vote'] ?? '';
    if (!$stream_id || !in_array($vote, ['up', 'down'])) {
        http_response_code(400); echo json_encode(['ok' => false]); exit;
    }
    $ip_hash = hashIp($_SERVER['REMOTE_ADDR'] ?? '');
    $votes   = loadSimpleVotes();
    $votes   = array_values(array_filter($votes, fn($v) =>
        !($v['ip_hash'] === $ip_hash && $v['stream_id'] === $stream_id)
    ));
    $votes[] = ['stream_id' => $stream_id, 'vote' => $vote, 'ip_hash' => $ip_hash, 'timestamp' => date('c')];
    $written = saveSimpleVotes($votes);
    if ($written === false) {
        http_response_code(500); echo json_encode(['ok' => false]); exit;
    }
    echo json_encode(['ok' => true, 'scores' => getScores($votes)]);
    exit;
}

// ── GET: debug (admin only, temporary) ────────────────────────────────────────
if ($method === 'GET' && $action === 'debug' && $key === ADMIN_KEY) {
    $raw = file_exists(DATA_FILE) ? file_get_contents(DATA_FILE) : null;
    $decoded = $raw ? json_decode($raw, true) : null;
    $statuses = $decoded ? array_map(fn($v) => $v['status'] ?? 'missing', $decoded) : [];
    $pending_count = $decoded ? count(array_filter($decoded, fn($v) => $v['status'] === 'pending')) : 0;
    echo json_encode([
        'file'          => DATA_FILE,
        'exists'        => file_exists(DATA_FILE),
        'count'         => $decoded ? count($decoded) : 0,
        'statuses'      => $statuses,
        'pending_count' => $pending_count,
    ]);
    exit;
}

// ── GET: list approved (public) ───────────────────────────────────────────────
if ($method === 'GET' && $action === 'list') {
    $data = loadData();
    $approved = array_filter($data, fn($v) => $v['status'] === 'approved');
    $byStream = [];
    foreach ($approved as $v) {
        $sid = $v['stream_id'];
        if (!isset($byStream[$sid])) $byStream[$sid] = [];
        if (count($byStream[$sid]) < 3) {
            $byStream[$sid][] = ['type' => $v['type'], 'reason' => $v['reason']];
        }
    }
    echo json_encode(['ok' => true, 'votes' => $byStream]);
    exit;
}

// ── GET: pending list (admin) ─────────────────────────────────────────────────
if ($method === 'GET' && $action === 'pending' && $key === ADMIN_KEY) {
    $data = loadData();
    $pending = array_values(array_filter($data, fn($v) => $v['status'] === 'pending'));
    echo json_encode(['ok' => true, 'votes' => $pending]);
    exit;
}

// ── POST: moderate (admin) ────────────────────────────────────────────────────
if ($method === 'POST' && $action === 'moderate' && $key === ADMIN_KEY) {
    $body = json_decode(file_get_contents('php://input'), true);
    $id  = $body['id'] ?? '';
    $act = $body['act'] ?? '';
    if (!$id || !in_array($act, ['approve', 'reject'])) {
        http_response_code(400); echo json_encode(['ok' => false]); exit;
    }
    $data = loadData();
    foreach ($data as &$v) {
        if ($v['id'] === $id) { $v['status'] = $act === 'approve' ? 'approved' : 'rejected'; break; }
    }
    saveData($data);
    echo json_encode(['ok' => true]);
    exit;
}

// ── POST: submit (public) ─────────────────────────────────────────────────────
if ($method === 'POST' && $action === 'submit') {
    $body      = json_decode(file_get_contents('php://input'), true);
    $stream_id = (int)($body['stream_id'] ?? 0);
    $title     = substr(trim($body['stream_title'] ?? ''), 0, 100);
    $type      = $body['type'] ?? '';
    $reason    = trim($body['reason'] ?? '');

    if (!$stream_id || !in_array($type, ['tried', 'researching', 'didnt_work'])) {
        http_response_code(400); echo json_encode(['ok' => false, 'msg' => 'Invalid input.']); exit;
    }
    if (strlen($reason) < 10) {
        http_response_code(400); echo json_encode(['ok' => false, 'msg' => 'Please write at least 10 characters.']); exit;
    }
    if (strlen($reason) > 300) {
        http_response_code(400); echo json_encode(['ok' => false, 'msg' => 'Max 300 characters.']); exit;
    }
    if (containsUrl($reason)) {
        http_response_code(400); echo json_encode(['ok' => false, 'msg' => 'Links are not allowed in submissions.']); exit;
    }

    $ip_hash = hashIp($_SERVER['REMOTE_ADDR'] ?? '');
    $data    = loadData();
    $cutoff  = time() - 86400;
    $recent  = array_filter($data, fn($v) =>
        $v['ip_hash'] === $ip_hash &&
        $v['stream_id'] === $stream_id &&
        strtotime($v['timestamp']) > $cutoff
    );
    if (count($recent) >= 1) {
        http_response_code(429); echo json_encode(['ok' => false, 'msg' => 'You already shared an experience for this stream today.']); exit;
    }

    $vote = [
        'id'           => uniqid('v_', true),
        'stream_id'    => $stream_id,
        'stream_title' => $title,
        'type'         => $type,
        'reason'       => $reason,
        'timestamp'    => date('c'),
        'ip_hash'      => $ip_hash,
        'status'       => 'pending',
    ];
    $data[] = $vote;
    $written = saveData($data);
    if ($written === false) {
        http_response_code(500);
        echo json_encode(['ok' => false, 'msg' => 'Save failed. Please contact site admin.']);
        exit;
    }
    echo json_encode(['ok' => true, 'msg' => 'Thank you! Your experience is under review.']);
    exit;
}

http_response_code(400);
echo json_encode(['ok' => false, 'msg' => 'Bad request']);
