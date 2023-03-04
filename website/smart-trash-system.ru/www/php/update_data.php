<?php

require_once("main.php");

if($_POST['access_id'] != '...') {
	echo 'wrong password';
	exit;
}

if($_POST['mode'] == 'create'){
    if(R::count('bins', 'bin_id = ?', array($_POST['bin_id'])) == 0){
	    $bin = R::dispense('bins');
	    $bin->bin_id = $_POST['bin_id'];
	    $bin->lat = $_POST['lat'];
	    $bin->lon = $_POST['lon'];
	    $bin->occupancy = $_POST['occupancy'];
	    R::store($bin);
        echo "bin created";
        exit;
    } else {
        echo "error";
        exit;
    }
} else if($_POST['mode'] == 'update') {
    if(R::count('bins', 'bin_id = ?', array($_POST['bin_id'])) == 1){
        $bin = R::load('bins', getBinId($_POST['bin_id']));
        $bin->bin_id = $_POST['bin_id'];
        $bin->occupancy = $_POST['occupancy'];
        R::store($bin);
	    echo "bin info updated";
        exit;
    } else {
        echo "error";
        exit;
    }
} else if($_POST['mode'] == 'update coords'){
    if(R::count('bins', 'bin_id = ?', array($_POST['bin_id'])) == 1){
        $bin = R::load('bins', getBinId($_POST['bin_id']));
        $bin->lat = $_POST['lat'];
	    $bin->lon = $_POST['lon'];
        R::store($bin);
	    echo "bin coords updated";
        exit;
    } else {
        echo "error";
        exit;
    }
} else {
    echo "error";
    exit;
}

?>