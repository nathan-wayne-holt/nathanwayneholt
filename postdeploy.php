<?php
	$secret = "SecretWebhookKey18593";
	
	if (!isset($_SERVER['HTTP_X_HUB_SIGNATURE'])) {
		echo "NOT SET";
		//throw new Exception('X-Hub-Signature missing.')
	} elseif (!extension_loaded('hash')) {
		echo "HASH NOT AVAILABLE";
		//throw new Exception('Hash extension not loaded.')
	}
	
	list($algorithm, $hash) = explode('=', $_SERVER['HTTP_X_HUB_SIGNATURE'], 2) + array('', '');
	
	$rawData = file_get_contents('php://input')
	
	if ($hash !== hash_hmac($algorithm, $rawData, $secret)) {
		echo "problem hashsing";
		//throw new Exception('Secret does not match hash.')
	}
	
	#Successfully passed secret into the header. Now run git pull.
	
	$output = shell_exec('git pull');
	echo $output;
	return $output;
?>