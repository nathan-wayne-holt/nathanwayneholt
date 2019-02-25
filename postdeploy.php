<?php
	$secret = "SecretWebhookKey18593";
	$hashed_secret = sha1($secret);
	$post_data = file_get_contents('php://input');
	
	if (!empty($post_data)) {
		echo "We're here!";
		shell_exec('cd ../ && git pull');
		$hashed_received = $_HEADER['X-Hub-Signature'];
		if ($hashed_received == $hashed_secret) {
			echo "SECRETS MATCH";
		} else{
			echo "do not match";
		}
		echo "pulled";
		//mail('nathanwayneholt@gmail.com', 'Auto-Deploy Activated', 'nathanwayneholt.com has auto-updated due to the detection that the remote repo has been updated.')
	}
?>