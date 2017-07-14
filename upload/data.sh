name=totem
insuf=.in
outsuf=.ans
for i in {1..10}
do
	mv $name$i$insuf $i.in
	mv $name$i$outsuf $i.out
done
zip $name.data.zip ./{*.in,*.out}
