lst=`ipcs -m -p|tail -n +4|cut -d ' ' -f1`
for key in $lst; do
    ipcrm -m $key
done
