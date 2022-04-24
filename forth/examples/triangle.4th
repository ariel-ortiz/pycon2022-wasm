( File: triangle.4th )
( Draws a triangle of stars of a size provided by the user. )

62 emit 32 emit ( Print prompt. )
input n!
1 i!
do
    i n <= ?
    i j!
    do
        j 0 > ?
        42 emit ( Print * )
        j 1 - j!
    loop
    nl
    i 1 + i!
loop
