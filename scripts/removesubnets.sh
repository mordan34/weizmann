#!/bin/sh

id=0

for id in {0..1250}
do
    hammer subnet update --domains "" --id $id
done
