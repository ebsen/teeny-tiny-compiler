# Teeny Tiny Compiler

Following along with [this fella](http://web.eecs.utk.edu/~azh/blog/teenytinycompiler1.html) to build a compiler for a pretend version of BASIC called Teeny Tiny. The compiler works in three stages:

1. The [lexer](http://web.eecs.utk.edu/~azh/blog/teenytinycompiler1.html), the which breaks the input code up into small pieces called tokens
2. The [parser](http://web.eecs.utk.edu/~azh/blog/teenytinycompiler2.html), which verifies that the tokens are in an order that our language allows
3. The emitter, which produces the appropriate C code