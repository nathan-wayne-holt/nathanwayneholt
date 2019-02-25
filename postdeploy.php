<?php
print_r($_POST, true);

	if (isset($_SERVER['HTTP_X_HUB_SIGNATURE'])) {
		echo $_SERVER['HTTP_X_HUB_SIGNATURE'];
		$message = "Received a payload. Did you make a push request?";
		mail("nathanwayneholt@gmail.com", "Push Received", $message);
		shell_exec('cd ../ && git pull');
	} else {
		echo "No payload was sent.";
	}
?>