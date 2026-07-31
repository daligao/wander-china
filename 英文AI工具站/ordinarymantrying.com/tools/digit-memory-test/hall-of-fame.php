<?php
define('SECRET',      'dmt_h0f_2026_xK9pQ3');
define('ADMIN_KEY',   'dmt_admin_2026_mX7vR5');   // change after upload!
define('DATA_FILE',   __DIR__ . '/hof_data.json');
define('RATE_FILE',   __DIR__ . '/hof_rate.json');
define('MIN_ELAPSED_12', 40);
define('MIN_ELAPSED_15', 55);
define('RATE_LIMIT',  5);    // max 5 submissions per IP per hour

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');

$action = $_GET['action'] ?? ($_POST['action'] ?? '');

function makeToken(int $ts): string {
    return hash_hmac('sha256', 'dmt_session_' . $ts, SECRET);
}

function loadData(): array {
    if (!file_exists(DATA_FILE)) return ['entries' => []];
    $d = json_decode(file_get_contents(DATA_FILE), true);
    return is_array($d) ? $d : ['entries' => []];
}

function saveData(array $data): void {
    file_put_contents(DATA_FILE, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), LOCK_EX);
}

function clean(string $s, int $max): string {
    return mb_substr(strip_tags(trim($s)), 0, $max);
}

function containsSpam(string $s): bool {
    $t = mb_strtolower($s);
    if (preg_match('/https?:\/\/|www\.|\.com|\.net|\.org|\.io|\.cn|\.cc/i', $t)) return true;
    if (preg_match('/@\w+\.\w/', $t)) return true;
    $digits = preg_replace('/[\s\-\.\(\)]/', '', $t);
    if (preg_match('/\d{7,}/', $digits)) return true;
    if (preg_match('/微信|威信|vx\s*[：:号]|wx\s*[：:]|qq\s*[：:]|telegram|whatsapp|扫码|加我|联系我|私聊|广告/u', $t)) return true;
    // Social media self-promotion
    if (preg_match('/follow\s+me|check\s+out|subscribe|my\s+channel|my\s+page|find\s+me|add\s+me|@[a-z0-9_]{3,}/i', $t)) return true;
    return false;
}

function checkRateLimit(): bool {
    $ip  = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $now = time();
    $rates = [];
    if (file_exists(RATE_FILE)) {
        $rates = json_decode(file_get_contents(RATE_FILE), true) ?: [];
    }
    foreach ($rates as $k => &$times) {
        $times = array_values(array_filter($times, fn($t) => $now - $t < 3600));
        if (empty($times)) unset($rates[$k]);
    }
    unset($times);
    $key = md5($ip);
    if (!isset($rates[$key])) $rates[$key] = [];
    if (count($rates[$key]) >= RATE_LIMIT) {
        file_put_contents(RATE_FILE, json_encode($rates), LOCK_EX);
        return false;
    }
    $rates[$key][] = $now;
    file_put_contents(RATE_FILE, json_encode($rates), LOCK_EX);
    return true;
}

function isTipsQuality(string $tips): bool {
    if ($tips === '') return true; // optional field
    if (mb_strlen($tips) < 15) return false;
    if (preg_match('/^(.)\1+$/u', trim($tips))) return false; // all same char
    return true;
}

switch ($action) {

    case 'init':
        $ts = time();
        echo json_encode(['token' => makeToken($ts), 'ts' => $ts]);
        break;

    case 'submit':
        $token   = $_POST['token']    ?? '';
        $ts      = intval($_POST['ts']      ?? 0);
        $elapsed = intval($_POST['elapsed'] ?? 0);
        $uname   = clean($_POST['username'] ?? '', 30);
        $country = clean($_POST['country']  ?? '', 60);
        $tips    = clean($_POST['tips']     ?? '', 200);

        if (!$ts || makeToken($ts) !== $token) {
            echo json_encode(['ok' => false, 'error' => 'Invalid session — please restart']); exit;
        }
        if ($elapsed < MIN_ELAPSED_12) {
            echo json_encode(['ok' => false, 'error' => 'Time looks suspicious — did you really play?']); exit;
        }
        if (mb_strlen($uname) < 2) {
            echo json_encode(['ok' => false, 'error' => 'Nickname must be at least 2 characters']); exit;
        }
        if (mb_strlen($country) < 2) {
            echo json_encode(['ok' => false, 'error' => 'Country is required']); exit;
        }
        if (containsSpam($uname) || containsSpam($tips) || containsSpam($country)) {
            echo json_encode(['ok' => false, 'error' => 'No links, handles, or contact info allowed']); exit;
        }
        if (!isTipsQuality($tips)) {
            echo json_encode(['ok' => false, 'error' => 'Memory tip too short (15+ chars) or invalid']); exit;
        }
        if (!checkRateLimit()) {
            echo json_encode(['ok' => false, 'error' => 'Too many submissions — try again later']); exit;
        }

        $data  = loadData();
        $id    = bin2hex(random_bytes(8));
        $entry = [
            'id'      => $id,
            'username'=> $uname,
            'country' => $country,
            'tips'    => $tips,
            'time12'  => $elapsed,
            'time15'  => null,
            'ts'      => time(),
        ];
        array_unshift($data['entries'], $entry);
        if (count($data['entries']) > 1000) {
            $data['entries'] = array_slice($data['entries'], 0, 1000);
        }
        saveData($data);
        echo json_encode(['ok' => true, 'id' => $id]);
        break;

    case 'update15':
        $id      = clean($_POST['id']      ?? '', 20);
        $token   = $_POST['token']  ?? '';
        $ts      = intval($_POST['ts']      ?? 0);
        $elapsed = intval($_POST['elapsed'] ?? 0);

        if (!$id || !$ts || makeToken($ts) !== $token) {
            echo json_encode(['ok' => false, 'error' => 'Invalid']); exit;
        }
        if ($elapsed < MIN_ELAPSED_15) {
            echo json_encode(['ok' => false, 'error' => 'Too fast']); exit;
        }

        $data  = loadData();
        $found = false;
        foreach ($data['entries'] as &$e) {
            if ($e['id'] === $id && $e['time15'] === null) {
                $e['time15'] = $elapsed;
                $found = true;
                break;
            }
        }
        unset($e);
        if ($found) saveData($data);
        echo json_encode(['ok' => $found]);
        break;

    case 'fetch':
        $data    = loadData();
        $entries = $data['entries'];

        $with15   = array_values(array_filter($entries, fn($e) => $e['time15'] !== null));
        $without15= array_values(array_filter($entries, fn($e) => $e['time15'] === null));
        usort($with15,    fn($a, $b) => $a['time15'] <=> $b['time15']);
        usort($without15, fn($a, $b) => $a['time12'] <=> $b['time12']);

        $merged = array_slice(array_merge($with15, $without15), 0, 50);
        $public = array_map(fn($e) => [
            'username' => $e['username'],
            'country'  => $e['country'],
            'tips'     => $e['tips'],
            'time12'   => $e['time12'],
            'time15'   => $e['time15'],
            'date'     => date('Y-m-d', $e['ts']),
        ], $merged);

        echo json_encode([
            'ok'      => true,
            'entries' => array_values($public),
            'total'   => count($entries),
        ]);
        break;

    case 'admin_list':
        if (($_GET['admin_key'] ?? '') !== ADMIN_KEY) {
            http_response_code(403); echo json_encode(['error' => 'Forbidden']); exit;
        }
        $data = loadData();
        echo json_encode(['ok' => true, 'entries' => $data['entries'], 'total' => count($data['entries'])]);
        break;

    case 'admin_delete':
        if (($_POST['admin_key'] ?? '') !== ADMIN_KEY) {
            http_response_code(403); echo json_encode(['error' => 'Forbidden']); exit;
        }
        $id   = clean($_POST['id'] ?? '', 20);
        $data = loadData();
        $before = count($data['entries']);
        $data['entries'] = array_values(array_filter($data['entries'], fn($e) => $e['id'] !== $id));
        $removed = $before - count($data['entries']);
        if ($removed > 0) saveData($data);
        echo json_encode(['ok' => true, 'removed' => $removed]);
        break;

    default:
        http_response_code(400);
        echo json_encode(['error' => 'Unknown action']);
}
