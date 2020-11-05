# Go features I don't use

Go is a simple language with a small amount of features. And still, there are some features that you don't need in your daily work. Some are needed only in a really performance-critical parts of the code, some have better alternatives, some are hard to use correctly. So, let's talk about such features. If we all agree that they aren't needed for regular projects, let's just name them as "advanced" and hide from our projects and beginners tutorials.

## Types

### complex{64,128}

### uint{8,16,32,64,} and int{8,16,32,64}

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

### print{ln,}

Functions `print` and `println` are [temporary hacks](https://golang.org/ref/spec#Bootstrapping) and can be removed from the language soon. Use [fmt](https://golang.org/pkg/fmt/) package instead.

### cap, imag, real

## Syntax

### Naked returns

### Non-ASCII names

### Type aliases

### Multiline comments

## Other

### Buffered Channels

### log.Fatalf
