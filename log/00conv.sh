#!/bin/sh

PCMBUSY="
adpcm_play_pcmbusy
adpcm_play2_pcmbusy
adpcm_play_limit_pcmbusy
"

MDEN="
adpcm_play_mden
adpcm_play2_mden
adpcm_play3_mden
adpcm_play4_mden
adpcm_play5_mden

adpcm_play_limit2_mden
adpcm_play_limit3_mden
adpcm_play_limit4_mden
adpcm_play_limit5_mden
adpcm_play_limit_mden

mem_rw_mden
mem_rw2_mden
mem_rw3_mden
mem_rw4_mden
mem_rw5_mden
mem_rw6_mden
"


conv()
{
    logs=$1
    opt=$2
    for l in $logs
    do
        echo $l
        cd $l
        bzcat $l.bin.bz2 | ../../logic-analyzer/towav $opt -o $l
        cd ..
    done
}

conv "$PCMBUSY" "-s"
conv "$MDEN" "-m"
