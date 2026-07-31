<?php
header('Content-Type: application/json; charset=utf-8');
session_start();

// Security: edit key validation (stored server-side only)
define('EDIT_KEY', 'k7f2m9v4x1q8n3j');
define('DATA_FILE', __DIR__ . '/daydayup-data.json');
define('SESSION_TIMEOUT', 3600); // 1 hour

$response = ['success' => false, 'message' => '', 'data' => []];

// Read existing data
function readData() {
    if (!file_exists(DATA_FILE)) {
        return [];
    }
    $json = file_get_contents(DATA_FILE);
    return json_decode($json, true) ?: [];
}

// Write data safely
function writeData($data) {
    $json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    $temp = DATA_FILE . '.tmp';

    if (file_put_contents($temp, $json) === false) {
        return false;
    }

    // Atomic rename
    return rename($temp, DATA_FILE);
}

// Check edit session validity
function isEditModeValid() {
    if (!isset($_SESSION['edit_mode_time'])) {
        return false;
    }
    if (time() - $_SESSION['edit_mode_time'] > SESSION_TIMEOUT) {
        unset($_SESSION['edit_mode_time']);
        return false;
    }
    return true;
}

$action = $_POST['action'] ?? '';

switch ($action) {
    case 'unlock':
        $key = $_POST['key'] ?? '';

        if ($key !== EDIT_KEY) {
            $response['message'] = 'Invalid edit key';
            break;
        }

        $_SESSION['edit_mode_time'] = time();
        $response['success'] = true;
        $response['message'] = 'Edit mode unlocked';
        break;

    case 'check-mode':
        $response['success'] = isEditModeValid();
        $response['edit_mode'] = $response['success'];
        break;

    case 'load':
        $data = readData();
        $response['success'] = true;
        $response['data'] = $data;
        break;

    case 'save':
        if (!isEditModeValid()) {
            $response['message'] = 'Unauthorized: Session expired or not authenticated';
            break;
        }

        $date = $_POST['date'] ?? '';
        $content = $_POST['content'] ?? '';

        // Validate date format (YYYY-MM-DD)
        if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $date)) {
            $response['message'] = 'Invalid date format';
            break;
        }

        $data = readData();

        if (trim($content) === '') {
            // Delete entry if empty
            unset($data[$date]);
        } else {
            // Save or update entry
            $data[$date] = $content;
        }

        if (writeData($data)) {
            $response['success'] = true;
            $response['message'] = 'Entry saved';
            $response['data'] = $data;
        } else {
            $response['message'] = 'Failed to write data';
        }
        break;

    case 'import':
        if (!isEditModeValid()) {
            $response['message'] = 'Unauthorized: Session expired or not authenticated';
            break;
        }

        $importedJson = $_POST['data'] ?? '';
        $imported = json_decode($importedJson, true);

        if (!is_array($imported)) {
            $response['message'] = 'Invalid JSON data';
            break;
        }

        // Merge or replace
        $existing = readData();
        $merged = array_merge($existing, $imported);

        if (writeData($merged)) {
            $response['success'] = true;
            $response['message'] = 'Import successful';
            $response['data'] = $merged;
        } else {
            $response['message'] = 'Failed to write data';
        }
        break;

    default:
        $response['message'] = 'Unknown action';
}

echo json_encode($response, JSON_UNESCAPED_UNICODE);
?>
