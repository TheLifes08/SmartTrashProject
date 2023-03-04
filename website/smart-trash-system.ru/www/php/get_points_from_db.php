<?php

header('Content-type: application/json');
require_once("main.php");

$array = getAllGpsPoints($_POST['lat'], $_POST['lon'], $_POST['k']);
echo json_encode($array);

?>