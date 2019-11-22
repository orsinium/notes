# Making arithmetic simpler

This is a place for experiments with arithmetic, based on [Steven Pemberton](https://en.wikipedia.org/wiki/Steven_Pemberton)'s talk [Programmers are humans too](https://homepages.cwi.nl/~steven/Talks/2019/11-21-dijkstra/).

## Addition

Definition: (a+1)+b = (a+b)+1
Commutativity: (a+b) = (b+a)
Fixed point: a+0 = a

## Substraction

Definition: (a+b)-b = a
Commutativity: nope
Monadic version: 0-a = -a

## Multiplication

Definition: (a+1)×b = a×b + b
Commutativity: a×b = b×a
Fixed point: a×1 = a

## Division

Definition: (a×b)÷b = a
Commutativity: nope
Monadic version: 1÷a = ÷a

## Properties

−−a = a
÷÷a = a

a−−b = a+b
a÷÷b = a×b

Commutability:

−(a−b) = (b−a)
÷(a÷b)  = (b÷a)

## Power

Definition: a↑(b+1) = (a↑b)×a
Commutativity: nope
Fixed point: a↑1 = a

## Root

Definition: (a↑b)↓b = a
Commutativity: nope
Fixed point: a↓1 = a

## Logarithm

Definition: (a↑b)⇓a = b
Commutativity: nope
Monadic version: 1⇓a = 0 ?

## More properties

a×(−b) = −(a×b)
a↑(−b) = ÷(a↑b)
a×(÷b) = a÷b
a↑(÷b) = a↓b
÷(a÷b) = b÷a
÷(a⇓b) = b⇓a
