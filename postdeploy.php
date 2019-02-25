<?php
	if (isset($_POST['payload'])) {
		$message = "Received a payload. Did you make a push request?";
		mail("nathanwayneholt@gmail.com", "Push Received", $message);
		shell_exec('cd ../ && git pull');
	} else {
		echo "No payload was sent.";
	}
?>