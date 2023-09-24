main: pyin.txt
	python3 main.py < pyin.txt
pyin.txt:
	gcc main.c -o main
	./main < cin.txt > pyin.txt 2> w_PLA.txt
clean:
	rm -f main pyin.txt w_PLA.txt

# histogram: main
# 	./main < cin.txt | python3 main.py
# main:
# 	gcc main.c -o main
# clean:
# 	rm -f main