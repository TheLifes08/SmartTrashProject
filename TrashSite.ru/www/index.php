<?php

$root = "";
require_once($root."php/main.php");

$page = new WebPage($root, "Умная мусорка$titlePostfix");
$page->favicon = "/images/favicon.ico";
$page->links = array(
	array("/styles/basics.css", "stylesheet", "text/css"),
	array("/styles/normalize.css", "stylesheet", "text/css"),
	array("https://use.fontawesome.com/releases/v5.6.3/css/all.css", "stylesheet", "text/css")
);
$page->scripts = array(
	"/scripts/libraries/jquery.js", 
	"/scripts/libraries/jquery-rotate.js", 
	"https://maps.googleapis.com/maps/api/js?key=AIzaSyDMe0aZgx84YzzaFsOeGgOsKQ6_BiJMr7c",
	"/scripts/main-page.js"
);
$page->language = "ru";
$page->extraTags = "
	<meta name='viewport' content='width=device-width, initial-scale=1'>
";

include($root."includes/head.php");
include($root."includes/header.php");

?>

<section id="content-section">
	<div id="map-div" onclick="hide_panel();">
	
	</div>
</section>

<div id="control_panel_map">
	<div>
		<span style="font-size: 13px;">Предельное расстояние:</span>
		<input id="radius-input"><br>
	</div>
	<div id="control_panel_map_button" class="pointer">
		Обновить метки
	</div>
</div>