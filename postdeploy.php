<?php
	if (isset($_POST['payload'])) {
		shell_exec('cd ../ && git pull');
	} else {
		echo "No payload was sent.";
	}
?>