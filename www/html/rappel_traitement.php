<?php

session_start();
#rappel_traitement.php?nom_alarme=thai&periodicite=heure&Lundi=on&Mercredi=on&Vendredi=on&tab1[]=12%3A30&message=YeY&color=bleu

print ("msg: ". $_POST['message'] . "\n");

$freq = 0;

print "horaire " . $_POST['horaire'];
echo "</br>";
print_r($_POST);
echo "</br>";

if (isset($_POST['Lundi']))
{
	$freq |= 128; 
}
if (isset($_POST['Mardi']))
{
	$freq |= 64; 
}
if (isset($_POST['Mercredi']))
{
	$freq |= 32; 
}
if (isset($_POST['Jeudi']))
{
	$freq |= 16; 
}
if (isset($_POST['Vendredi']))
{
	$freq |= 8; 
}
if (isset($_POST['Samedi']))
{
	$freq |= 4; 
}
if (isset($_POST['Dimanche']))
{
	$freq |= 2; 
}

$conf = $_POST['nom_alarme'] . "+" . strval($freq) . "+" . $_POST['horaire'] . "+"  . $_POST['color'] . "\n";

print ("conf: " . $conf);

file_put_contents("/var/www/html/obsy.conf", $conf, FILE_APPEND);

#if (!isset($_POST['nom_alarme']) || !preg_match("/^.+@.+\..+$/", $_POST['mail']))
?>
