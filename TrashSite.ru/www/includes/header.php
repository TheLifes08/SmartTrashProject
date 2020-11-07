<body>
	<section id="header-section" class="flex">
		<div id="header-left-div">
			<div id="header-left-head-div">
				<img id="logo-img" src="<?php echo $root."images/logo.png"; ?>">
			</div>
            
            
			<div id="header-town-div" class="center">
                    <span>Город: </span>
					<select style="margin-left: 5px;" id="select_city" onchange="change_city(this.options[this.selectedIndex].value);">
						<?php
							$cities = getCities();
							print_r($cities);
							for($i = 0; $i < count($cities); $i++){
								echo "<option value='".$cities[$i]."'>".$cities[$i]."</option>";
							}
						?>
					</select>
                </div>
            
			<div id="bin-list">
                <div id="search-div" class="flex">
					<div id="search-input-div">
						<input id="search-input">
					</div>
					<div id="search-input-button" class="center transition-effect pointer" tabindex="0">
						<i class="fas fa-search"></i>
					</div>
				</div>
                <ul id="trashlist">
                    <li class="trashlist-object">
                        <div class="trash-status">
                            <p class="trash-status-percents">87%</p>
                            <i class="fas fa-trash" style="color: #d33900"></i>
                        </div>
                        
                        <div class="trash-object-info">
                            <div class="trash-object-address">
                                <p>ул. Ленинградская, д. 7</p>
                            </div>
                        </div>
                    </li>
                </ul>
			</div>
		</div>
		<div id="header-right-div">
			<div id="menu-button" class="center transition-effect pointer">
                <i class="fas fa-bars"></i>
			</div>
		</div>
	</section>