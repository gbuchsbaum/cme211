# 1.1 Vocabulary
## A:
1. `int n;` Declare integer `n`
2. `n = 0;` Set value of `n` to 0
3. `int f( void );` Declare a function named `f()` that takes no arguments and returns an integer
4. `int f( void ) { /* insert sub - routine contents here . */ }` Define the functionality of `f()` with the code contained in `{ }`

## B:
Statically typed means that once a variable or object has been declared as one type, it cannot be subsequently changed to another type.

Strongly typed means that variables are defined as a specific type, and can only perform the actions allowed by that type.

`int pi = 3.14;` compiles without error because C++ allows some implicit conversions (i.e. it can convert a `double` to an `int` by removing all digits after the decimal point).

## C:
`int a[4];`

"Statically allocated" in this context means that the array size is known at compile time.

## D:
This function adds all positive integers less than `n`.

It could be improved by initializing the value of `sum` (presumably a value of 0) or by starting the loop with `int i = 1;` since adding 0 does nothing except take extra time.

## E:
The statement on line 3 is a constructor.

It returns an `S` object with an `s` value of 42, and is used when declaring a new `S`.

# 1.2 Data Types

## A:

## B:
This would likely produce a conversion error, as it would be trying to compare an `int` to an `unsigned int` (since the result of the `size()` function is unsigned).

## C:
The variable's value is not well-defined. It is not initialized with a value, so its value is just whatever was previously stored in that particular memory location the variable is assigned to.

## D:

# 1.3 C-Style Strings:
`const` refers to the character in the location referenced by `str` (i.e. the address `str` looks to can change, but the value at that address cannot).

The location that str is pointing to is incremented and the value at that location is dereferenced. The while loop continues this until the location references a null value.

The computational work is of order n (proportional to the input argument size). The input argument size is the length of the string that `*str` is pointing to.

# 1.4 Compilers:
This error is due to the compiler not knowing to include foo.hpp or foo.cpp. The correct syntax is `g++ -std=c++11 main.cpp foo.hpp foo.cpp -o main`.

# 1.5 Memory and Segfaults:
No output is guaranteed. We should expect an output of 0, but only if there happens to be extra space next to the space allocated for `arr`.

This can be compiled, since there are no syntax errors.

This program is likely to run, as the address being referenced is close enough to the memory addresses set aside for `arr` that the space should be available.

valgrind can be used to check for memory issues.