# Go features I don't use

Go is a simple language with a small amount of features. And still, there are some features that you don't need in your daily work. Some are needed only in a really performance-critical parts of the code, some have better alternatives, some are hard to use correctly. So, let's talk about such features. If we all agree that they aren't needed for regular projects, let's just name them as "advanced" and hide from our projects and beginners tutorials.

## Types

### complex{64,128}

For some reason, some languages have [complex numbers](https://en.wikipedia.org/wiki/Complex_number) right among the built-in types. And Go isn't an exception:

```go
n := 2+3i
fmt.Println(n + 3)
// Output: (5+3i)
```

To bo honest, I never used complex numbers in my code. Sure, there are helpful for many scientific applications, so it would be helpful to have them in [math](https://golang.org/pkg/math/) package and keep in built-ins only the most important things. After all, golang is designed not for science. Yes, having complex numbers as a `struct` would make math operation on it not so beautiful (because Go has no operator overload) but the question is why complex numbers are any special? Go has no a type for matrices, sets, rational numbers. Is support for complex numbers more important?

### uint{8,16,32,64,}

Did you ever think [why len returns int instead of uint](https://stackoverflow.com/questions/39088945/why-does-len-returned-a-signed-value)? Array index is int, so is len. And array index is int because uint is easy to overflow:

```go
ui := uint32(4)
fmt.Println(ui-17)
// Output: 4294967283
```

So, using uint can lead to unexpected values and obscure errors. Be careful when using it.

### int{8,16,32,64}

### array

## Functions

### panic

### recover

### new

Function `new` allocates a zero-value of a type in the memory and returns a pointer on it. It's [not really useful](https://stackoverflow.com/a/9322182) and always can be replaced by another way of memory allocation:

```go
// with new:
f := new(File)
// without new:
f := &File{}
```

It is shorter only for getting an adress for non-composite literal but it's hard to imagine a case when it is useful:

```go
// with new:
return new(i)

// without new:
var i int
return &i
```

### var x = something

### print{ln,}

Functions `print` and `println` are [temporary hacks](https://golang.org/ref/spec#Bootstrapping) and can be removed from the language soon. Use [fmt](https://golang.org/pkg/fmt/) package instead.

### cap, imag, real

## Syntax

### goto

### Labels

### else

### Positional struct fields

### Naked returns

### Non-ASCII names

### Type aliases

### Multiline comments

### Assignment inside if condition

### Tuple assignment

### go

### Non-decimal forms of int literal

## Other

### init

### Buffered Channels

### log.Fatalf
