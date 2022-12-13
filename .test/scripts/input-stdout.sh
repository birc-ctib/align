out=$(mktemp /tmp/ctib.XXXXXX)
function cleanup { rm $out ; }
trap cleanup EXIT

python3 src/main.py from_cig data/cigs.in > $out
.test/scripts/cmp.sh $out data/cigs.out || exit 1

python3 src/main.py to_cig data/alignments.in > $out
.test/scripts/cmp.sh $out data/alignments.out || exit 1
