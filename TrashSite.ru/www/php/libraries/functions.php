<?php

	function connectDB($db_host, $db_name, $db_user, $db_pass){
		$db = R::setup("mysql:host=$db_host;dbname=$db_name", $db_user, $db_pass);
		
		if(!R::testConnection())
			echo "Отсутствует подключение к базе данных!";
		
		return $db;
	}
	
	function getAllGpsPoints($lat, $lon, $k){
		return R::getAll('SELECT * FROM bins WHERE (POW('.(string)($k).', 2) >= POW(ABS(lat - '.(string)($lat).'), 2) + POW(ABS(lon - '.(string)($lon).'), 2))');
	}

	function getBinId($bin_id){
		return (R::findOne('bins', 'bin_id = ?', array($bin_id)))->id;
	}
	
	function getCities(){
		return R::getCol('SELECT city FROM cities');
	}

?>