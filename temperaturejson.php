<?php
 
$username="myuser";
$password="mypass123";
$database="sensehat";
 
mysql_connect(localhost,$username,$password);
@mysql_select_db($database) or die( "Unable to select database");
 
$query="SELECT * FROM envdata";
$result=mysql_query($query);
 
$num=mysql_numrows($result);
 
mysql_close();
 
$tempValues = array();
 
$i=0;
while ($i < $num)
{
        $dateAndTemps = array();
        $datetime=mysql_result($result,$i,"time");
        $temp=mysql_result($result,$i,"temperature_from_humidity");
 
        $dateAndTemps["Date"] = $datetime;
        $dateAndTemps["Temp"] = $temp;
 
        $tempValues[$i]=$dateAndTemps;
        $i++;
}
 
echo json_encode($tempValues);
 
?>