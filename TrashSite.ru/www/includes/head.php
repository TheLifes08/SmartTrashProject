<!DOCTYPE html>
<html>
	<head>
		<?php 
			if(isset($page->contentType)){ 
				if(isset($page->charset)){ 
					echo "<meta http-equiv='Content-Type' content='$page->contentType; charset=$page->charset'>"; 
				} else { 
					echo "<meta http-equiv='Content-Type' content='$page->contentType; charset=UTF-8'>"; 
				} 
			} else { 
				if(isset($page->charset)){ 
					echo "<meta charset='".$page->charset."'>"; 
				} else { 
					echo "<meta charset='UTF-8'>"; 
				} 
			} 
		?>
		<title><?php if(isset($page->title)){ echo $page->title; } else { echo "Unknown page"; } ?></title>
		
		<?php
		
			if(isset($page->description)){
				echo "<meta name='description' content='$page->description'>";
				echo "<meta http-equiv='description' content='$page->description'>";
			}
			
			if(isset($page->keywords)){
				echo "<meta name='keywords' content='$page->keywords'>";
				echo "<meta http-equiv='keywords' content='$page->keywords'>";
			}
			
			if(isset($page->favicon)){
				echo "<link href='$page->favicon' rel='shortcut icon' type='image/x-icon'>";
			}
			
			if(isset($page->language)){
				echo "<meta http-equiv='Content-Language' content='$page->language'>";
			}
			
			if(isset($page->extraTags)){
				echo $page->extraTags;
			}
			
			if(isset($page->links)){
				foreach($page->links as $link){
					echo '<link href="'.$link[0].'" rel="'.$link[1].'" type="'.$link[2].'"/>';
				}
			}
			
			if(isset($page->scripts)){
				foreach($page->scripts as $script)
					echo '<script type="text/javascript" src="'.$script.'"></script>';
			}
		
		?>
	</head>