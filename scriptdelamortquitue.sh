#!/bin/bash

MY_IP="`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p' | tail -1`"

echo "<?php

#rappel_traitement.php?nom_alarme=thai&periodicite=heure&Lundi=on&Mercredi=on&Vendredi=on&tab1[]=12%3A30&message=YeY&color=bleu

\$postdata = http_build_query(
    array(
        'nom_alarme' => 'thai',
        'periodicite' => 'heure',
		'Lundi' => 'on',
		'tab1' => '12:30',
		'message' => 'Yey',
		'color' => 'bleu'
    )
);

\$opts = array('http' =>
    array(
        'method'  => 'POST',
        'header'  => 'Content-type: application/x-www-form-urlencoded',
        'content' => \$postdata
    )
);

\$context  = stream_context_create(\$opts);

\$result = file_get_contents('http://${MY_IP}/rappel_traiement.php', false, \$context);
?>" > /var/www/html/post.php



