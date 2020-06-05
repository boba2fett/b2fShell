<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");


function featureLog($out, $cwd, $cmd) {
    $datum = date('Y').'-'.date('m').'-'.date('d');
    $time=date('H').'-'.date('i').'-'.date('s');
    mkdir('p0wny_log/');
    mkdir('p0wny_log/'.$datum.'/');
    $fcmd = @fopen('p0wny_log/'.$datum.'/'.$time.'_cmd', 'w');
    $fout = @fopen('p0wny_log/'.$datum.'/'.$time.'_out', 'w');


    if ($fcmd === FALSE || $fout === FALSE) {
        return array(
            'stdout' => array('Could Not Log')
        );
    } else {
        fwrite($fcmd, $cwd.' '.$cmd);
        fclose($fcmd);

        fwrite($fout, $out);
        fclose($fout);
        return array(
            'stdout' => array('Logged')
        );
    }
}


if (isset($_GET["feature"])) {

    $response = NULL;

    switch ($_GET["feature"]) {
        case 'log':
            $response = featureLog($_POST['out'], $_POST['cwd'], $_POST['cmd']);
    }

    header("Content-Type: application/json");
    echo json_encode($response);
    die();
}
?>
