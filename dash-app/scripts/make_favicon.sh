
mkdir -p tmp
for s in {16,32,48,128,256}; do
    convert icon_src.png -scale $s tmp/$s.png
done

convert tmp/16.png tmp/32.png tmp/48.png tmp/128.png tmp/256.png favicon.ico
rm -rf tmp
