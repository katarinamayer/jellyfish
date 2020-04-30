# !/bin/bash
# Excute this from within cs419-project/jellyfish

DIR="perftest/results/results_20hosts_"
for x in {1..30}
do
	if [ -d "$DIR$x" ]; then
		continue
	else
		mkdir "$DIR$x"
		echo "created new directory $DIR$x"

		cp perftest/results/*.txt "$DIR$x"
		sudo rm perftest/results/*.txt
		echo "moved test files into $DIR$x"

		break

	fi
done

