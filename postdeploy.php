<?php
	$post_data = file_get_contents('php://input');
	
	if (!empty($post_data)) {
		shell_exec('cd ../ && git pull');
		mail('nathanwayneholt@gmail.com', 'Auto-Deploy Activated', 'nathanwayneholt.com has auto-updated due to the detection that the remote repo has been updated.')
	}
?>