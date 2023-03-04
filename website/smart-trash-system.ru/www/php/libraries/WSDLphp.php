<?php

class WebPage {
	public $title;
	public $charset;
	public $description;
	public $keywords;
	public $links;
	public $scripts;
	public $rootHref;
	public $favicon;
	public $language;
	public $contentType;
	public $extraTags;
	
	public function __construct($rootHref_, $title_){
		$this->rootHref  = $rootHref_;
		$this->title = $title_;
	}
}


?>