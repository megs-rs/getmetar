#!/bin/bash
for x in `ls 2021*.txt` 
do 
   echo arquivo: $x 
   echo -n 'inicio:  ';head -n 1 $x| cut -b26-44 
   echo -n 'fim:     ';tail -n 1 $x| cut -b26-44 
   echo
done
