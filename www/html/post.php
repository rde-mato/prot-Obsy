<?php

#rappel_traitement.php?nom_alarme=thai&periodicite=heure&Lundi=on&Mercredi=on&Vendredi=on&tab1[]=12%3A30&message=YeY&color=bleu

$postdata = http_build_query(
    array(
        'nom_alarme' => 'thai',
        'periodicite' => 'heure',
		'Lundi' => 'on',
		'tab1' => '12:30',
		'message' => 'Yey',
		'color' => 'bleu'
    )
);

$opts = array('http' =>
    array(
        'method'  => 'POST',
        'header'  => 'Content-type: application/x-www-form-urlencoded',
        'content' => $postdata
    )
);

$context  = stream_context_create($opts);

$result = file_get_contents('http://10.18.190.103/rappel_traiement.php', false, $context);
?>
