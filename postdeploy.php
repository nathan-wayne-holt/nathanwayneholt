<?php
	$post_data = file_get_contents('php://input');
	echo $post_data;
	shell_exec('cd ../ && git pull');
?>