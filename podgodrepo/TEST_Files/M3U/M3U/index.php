<?php
header('Content-Type: application/xml; charset=utf-8');

/* RSS 2.0 MP3 SUBSCRIPTION FEED
	
	 "mp3feed.php" - version 1.1
	 2005 - Canton Becker - canton@gmail.com
	 
	 Yeah, it's pretty basic. 
	 But it's free.
	 Here's where to get the latest version:
	 http://www.cantonbecker.com/canton/projects

	 Use at your own risk, or don't use it at all...
	 
*/

// CONFIGURE THESE VARIABLES:

// actual place where your mp3s live on your server's filesystem. TRAILING SLASH REQ'D.
$musicDirectory=realpath(dirname(__FILE__));
$musicDirectory = $musicDirectory . "//";

// corresponding web URL for accessing the music directory. TRAILING SLASH REQ'D.
$musicURL=curPageURL();

// name your feed
$feedTitle="My Feeds";

// where every entry in your feed will link to, sort of like a "for more info" link
$feedLink="#";

// describe your feed
$feedDescription="My First Show";

// outline your copyright / creative commons / licensing terms
$feedCopyright="2013, Your Station";

// your email... if you dare!
$authorEmail="myemail@mywebsite.com";

// how often should feed readers check for new material (in seconds) -- mostly ignored by readers.
$ttl = 1440;

// END OF STUFF YOU NEED TO CONFIGURE!

function curPageURL() {
	$pageURL = "http://" . $_SERVER["SERVER_NAME"].$_SERVER["REQUEST_URI"];
 return $pageURL;
}

echo "<?xml version=\"1.0\" encoding=\"utf-8\"?>\r";
?>

<!-- generator="alien-green-chile-technology/1.1" -->

<rss version="2.0">
  <channel>
    <title><?php echo $feedTitle; ?></title>
    <link><?php echo $feedLink; ?></link>
    <description><?php echo $feedDescription; ?></description>
    <language>en</language>
	<copyright><?php echo $feedCopyright; ?></copyright>
	<ttl><?php echo $ttl; ?></ttl>
<?php
// step through each item...
	$fileDir = opendir($musicDirectory) or die ($php_errormsg);
	while (false !== ($thisFile = readdir($fileDir))){
		$thisFilePath = $musicDirectory . $thisFile;
			if (is_file($thisFilePath) && strrchr (strtolower($thisFilePath), '.') == ".mp3") {
				$myFullURL=$musicURL . $thisFile;
				$myFileSize=filesize($thisFilePath);
				$filedate = date("F d Y H:i:s.", filectime($thisFilePath));
?>
		<item>
			<title><?php echo ucwords(strtolower($thisFile)); ?></title>
			<link><?php echo $feedLink; ?></link>
			<description><?php
			//we have a description file here?
			$thisTextPath = substr_replace($thisFilePath, ".txt", (strlen($thisFilePath) - 4));
			if (is_file($thisTextPath)) {
				$textContents = file($thisTextPath);
				foreach ($textContents as $thisLine) echo htmlspecialchars($thisLine) . "\n";
			} ?></description>
			<enclosure url="<?php echo $myFullURL; ?>" length="<?php echo $myFileSize; ?>" type="audio/mpeg" />
			<guid><?php echo $myFullURL; ?></guid>
			<author><?php echo $authorEmail; ?></author>
			<pubDate><?php echo $filedate; ?></pubDate>
		</item>
	<?php
	}
}
closedir($fileDir);
?>
  </channel>
</rss>