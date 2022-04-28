( File: 1_to_10.4th )
( Display numbers 1 to 10, each number in its own line. )

1 x!          ( Initialize x with 1. )
do
    x 10 <= ? ( Continue in loop while x is less than or equal to 10. )
    x . nl    ( Print current value of x on its own line. )
    x 1 + x!  ( Increment in one the value of x. )
loop
