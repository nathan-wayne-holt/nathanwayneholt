<?php
	$post_data = file_get_contents('php://input');
	
	if (!empty($post_data)) {
		echo "We're here!";
		shell_exec('cd ../ && git pull');
		echo "pulled";
		//mail('nathanwayneholt@gmail.com', 'Auto-Deploy Activated', 'nathanwayneholt.com has auto-updated due to the detection that the remote repo has been updated.')
	}
?>