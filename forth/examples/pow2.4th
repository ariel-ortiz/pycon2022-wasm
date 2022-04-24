( File: pow2.4th )
( Prints all the powers of two from 0 to a user provided value. )

62 emit 32 emit ( Print prompt. )
input n!
0 i!
do
    i n <= ?
    1 r!
    1 j!
    do
        j i <= ?
        r 2 * r!
        j 1 + j!
    loop
    2 . 94 emit 32 emit i . 61 emit 32 emit r . ( Print: 2 ^ i = r )
    nl
    i 1 + i!
loop
