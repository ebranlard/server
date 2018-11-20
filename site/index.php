<html>
<head>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
<?php


// --------------------------------------------------------------------------------
// ---  
// --------------------------------------------------------------------------------
$log='';
$sent='';
$time=9999;
$volume=0.9999;
$FileTestSound  = '_listen/alarm_test_set' ;
$FileAlarmSet   = '_listen/alarm_info_set' ;
$FileMusicStop  = '_listen/music_stop' ;
$FileMusicStart = '_listen/music_start';
$FileMusicDown  = '_listen/music_down';
$FileMusicUp    = '_listen/music_up';
$FileLog        = '_data/log.txt';
$FileAlarmInfo  = '_data/alarm_info.txt' ;
$serverProcessName = 'server.sh';



// --------------------------------------------------------------------------------
// --- Functions for ini 
// --------------------------------------------------------------------------------
function write_php_ini($array, $file,$section_name)
{
    $res = array();
    $res[] = "[".$section_name."]";
    foreach($array as $key => $val)
    {
        if(is_array($val))
        {
            $res[] = "[$key]";
            foreach($val as $skey => $sval) $res[] = "$skey = ".(is_numeric($sval) ? $sval : '"'.$sval.'"');
        }
        else $res[] = "$key = ".(is_numeric($val) ? $val : '"'.$val.'"');
    }
    safefilerewrite($file, implode("\r\n", $res));
}

function safefilerewrite($fileName, $dataToSave)
{    if ($fp = fopen($fileName, 'w'))
    {
        $startTime = microtime(TRUE);
        do
        {            $canWrite = flock($fp, LOCK_EX);
           // If lock not obtained sleep for 0 - 100 milliseconds, to avoid collision and CPU load
           if(!$canWrite) usleep(round(rand(0, 100)*1000));
        } while ((!$canWrite)and((microtime(TRUE)-$startTime) < 5));

        //file was locked so now we can store information
        if ($canWrite)
        {            fwrite($fp, $dataToSave);
            flock($fp, LOCK_UN);
        }
        fclose($fp);
    }

}
// --------------------------------------------------------------------------------
// ---  
// --------------------------------------------------------------------------------
function processExists($processName) {
    $exists = false;
    exec("ps -A| grep -i $processName | grep -v grep", $pids); 
    if (count($pids) >0) {
        $exists = true;
    }
    return $exists;
}


// --------------------------------------------------------------------------------
// --- Music 
// --------------------------------------------------------------------------------
$IP='127.0.0.1';
$PORT=5005;
if (!empty($_POST["TestUDP"]))  {
        $sent="TestUDP";
        $msg = "Png !";
        $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
        socket_sendto($sock, $msg, strlen($msg), 0, $IP,$PORT);
        socket_close($sock);
}

if (!empty($_POST["MusicStop"]))  {
        $sent="Music stop";
        #file_put_contents($FileMusicStop,"");
        $msg = "MusicStop";
        $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
        socket_sendto($sock, $msg, strlen($msg), 0, $IP,$PORT);
        socket_close($sock);
}
if (!empty($_POST["MusicStart"]))  {
        $sent="Music start";
        #file_put_contents($FileMusicStart,"");
        $msg = "MusicStart";
        $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
        socket_sendto($sock, $msg, strlen($msg), 0, $IP,$PORT);
        socket_close($sock);
}
if (!empty($_POST["MusicUp"]))  {
        $sent="Volume Up";
        #file_put_contents($FileMusicUp,"");
        $msg = "VolUp";
        $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
        socket_sendto($sock, $msg, strlen($msg), 0, $IP,$PORT);
        socket_close($sock);
}
if (!empty($_POST["MusicDown"]))  {
        $sent="Volume Down";
        #file_put_contents($FileMusicDown,"");
        $msg = "VolDown";
        $sock = socket_create(AF_INET, SOCK_DGRAM, SOL_UDP);
        socket_sendto($sock, $msg, strlen($msg), 0, $IP,$PORT);
        socket_close($sock);
}

// --------------------------------------------------------------------------------
// ---  Alarm
// --------------------------------------------------------------------------------
if (!empty($_POST["test_sound"]) or !empty($_POST["change_alarm"]))  {
    $ini_array["Time"]  =$_POST["Time"];
    $ini_array["Volume"]=$_POST["Volume"]/100;
    write_php_ini($ini_array,$FileAlarmInfo,"alarm_info");

    if (!empty($_POST["test_sound"])) {
        $sent="test_sound command";
        file_put_contents($FileTestSound,"");
    }
    if (!empty($_POST["change_alarm"]))  {
        $sent="change_alarm command";
        file_put_contents($FileAlarmSet, "");
//         $fid = fopen("alarm_info_set", "w") or die("Unable to open file info set!");
//         fwrite($fid, "1");
//         fclose($fid);
    }
}
if (file_exists($FileAlarmInfo)) {
    $ini_array = parse_ini_file($FileAlarmInfo);
    $time   = $ini_array["Time"]  ;
    $volume = $ini_array["Volume"]*100;
}


if (!empty($_POST["clearlog"])){
    $sent="clear command";
//     file_put_contents($FileLog, "");
    $fid = fopen($FileLog, "w") or die("Unable to reset log file!");
    fwrite($fid, "");
    fclose($fid);

}

// $log=file_get_contents($FileLog);
if (!empty($_POST["showlog"])){
    $log=file_get_contents($FileLog);
}

if (!processExists($serverProcessName)){
    echo "The server is offline!<br>";
}
?>

<!-- ------------------- MUSIC --------------------- -->
<form action="index.php" method="post">
<input type="submit" name="MusicStart"  value='Start Music'/>
<input type='submit' name="MusicStop" value='Stop Music'/>
<input type='submit' name="MusicUp"   value='+'/>
<input type='submit' name="MusicDown" value='-'/>
</form>

<!-- ------------------- LOG --------------------- -->
<br>
Log: <?=$sent;?><br>
<form action="index.php" method="post">
<input type='submit' name="clearlog" value='Clear Log'/>
<input type='submit' name="showlog" value='Show Log'/>
</form>

<script type="text/javascript">
// <input type='button' onclick='changeText()' value='Show Log'/>
function changeText(){
    document.getElementById('LogPane').innerHTML = '<object type="text/html" data="_data/log.txt"></object>'
}
// function updateTextInput(val) {
//           document.getElementById('textInput').value=val; 
//         }
</script>
<div id='LogPane'><?php echo $log;?></div>

<!-- ------------------- ALARM --------------------- -->
<br>
<form action="index.php" method="post">
<label>Time  : </label>
 <input type="time" name="Time" value="<?=$time;?>">
<br>
<label>Volume  : </label>
<input type="range" min="1" max="99" step="5"/ name="Volume" value=<?=$volume;?>>
<br>
<input type="submit" name="change_alarm" value='Set Alarm'/>
<input type='submit' name="test_sound" value='Test Now'/>
</form>
</body>
</html> 
