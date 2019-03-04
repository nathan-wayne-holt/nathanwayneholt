<?php
	//echo "testing";

	$secret = "SecretWebhookKey18593";
	
	if (!isset($_SERVER['HTTP_X_HUB_SIGNATURE'])) {
		echo "NOT SET";
		//throw new Exception('X-Hub-Signature missing.')
	} elseif (!extension_loaded('hash')) {
		echo "HASH NOT AVAILABLE";
		//throw new Exception('Hash extension not loaded.')
	}
	$raw = file_get_contents('php://input');
	
	list($algorithm, $hash) = explode('=', $_SERVER['HTTP_X_HUB_SIGNATURE'], 2) + array('', '');
	
	if ($hash !== hash_hmac('sha1', $raw, $secret)) {
		echo "problem hashing";
		//throw new Exception('Secret does not match hash.')
	}
	
	#Successfully passed secret into the header. Now run git pull.
//	echo shell_exec('git status');	
	echo shell_exec('sudo git pull');
	
	echo "successfully pulled?";
?>
