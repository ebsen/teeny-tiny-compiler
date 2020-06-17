# `make hello` => Compile hello.tiny into hello.c compiled into hello object code automagically.
%.c : %.tiny
	python3 ./teenytiny.py $< > $@
