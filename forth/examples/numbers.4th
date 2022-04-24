( File: numbers.4th )
( Adds and multiplies two user provided numbers. )

62 emit 32 emit ( Print first prompt. )
input x!

62 emit 32 emit ( Print second prompt. )
input y!

( Print: x + y = result )
x . 43 emit 32 emit y . 61 emit 32 emit x y + . nl

( Print: x * y = result )
x . 42 emit 32 emit y . 61 emit 32 emit x y * . nl
