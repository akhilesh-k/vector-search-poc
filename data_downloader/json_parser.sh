#!/bin/bash
i=0
file=0
for f in `cat solr_result.json | jq -c -M '.[]'`;
do

   if [ $i -eq 5000 ]; then

         ret=`jq --slurp "." /tmp/0.json /tmp/1.json  > File$file.json`;
         ret=`rm /tmp/0.json /tmp/1.json`; #cleanup

         ((file = file + 1));
     i=0
   fi
   ret=`echo $f > /tmp/$i.json`;
   ((i = i + 1));
done
if [ -f /tmp/0.json ]; then
    ret=`jq --slurp '.' /tmp/0.json > File$file.json`;
    ret=`rm /tmp/0.json`; #cleanup
fi