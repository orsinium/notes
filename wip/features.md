# [WIP] Go features I don't use

(This article is in progress)

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

Don't panic! Function `panic` is intended for exceptions that should not be catched, stating that something required for program to work is broken (like memory corruption) and the application can't do anything about it. The thing is that your code unlikely to have any of such cases. Can't commect to database? Try again a bit later. Unknown option is passed? Return an error to the user.

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

Did you know that Go has operator `goto`? There is famous article by Edsger Dijkstra named "[Go To Statement Considered Harmful](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf)". This is an important publication that started transformation of languages to have and prefer alternative flow control constructions, like `switch`, `for`, `while`, `until`, `break`, `continue`. It is proven that any flow can be represented without `goto`. Read [Goto Criticism](https://en.wikipedia.org/wiki/Goto#Criticism) for more context.

### Labels

Labels are used by `goto`, `break`, and `continue` to show to which point the execution context must be switched. The thing is that using it with `continue` or `break` is the same as `goto`: unnecesary, dangerous, and hard to read. If you have a ces where you want to break through a few nested for-loops, extract this part into a separate function and use `return` statement instead.

Bad:

```go
func something() {
    do_before()
    Loop:
        for _, ch := range "a b\nc" {
            switch ch {
            case ' ': // skip space
                break
            case '\n': // break at newline
                break Loop
            default:
                fmt.Printf("%c\n", ch)
            }
        }
    do_after()
}
```

Good:

```go
func something() {
    do_before()
    iterate()
    do_after()
}

func iterate() {
    for _, ch := range "a b\nc" {
        switch ch {
        case ' ': // skip space
            continue
        case '\n': // break at newline
            return
        default:
            fmt.Printf("%c\n", ch)
        }
    }
}
```

### fallthrough

Statement `fallthrough` allows to execute the body of the next `case` in `switch` without checking the condition. This is the same story as with labels: if a few condition branches share the same behavior, extract this behavior into a separate function.

Bad:

```go
func something() {
    switch 2 {
    case 1:
        fmt.Println("1")
        fallthrough
    case 2:
        fmt.Println("2")
        fallthrough
    case 3:
        fmt.Println("3")
    }
    do_after()
}
```

Good:

```go
func something() {
    switch 2 {
    case 1:
        fmt.Println("1")
        common()
    case 2:
        fmt.Println("2")
        common()
    case 3:
        common()
    }
    do_after()
}

func common() {
    fmt.Println("3")
}
```

### Dot imports

...

### else

### Positional struct fields

### Naked returns

### Non-ASCII names

### Type aliases

### Multiline comments

Go has 2 types of comments:

```go
// inline

/*
and multiline
*/
```

Most likely, your IDE has a hotkey to comment out the selected snippet. Try `ctrl+/`, it should work. It will use inline comments syntax and it works great. Use it and forget about multiline comments syntax and manually writing `//`.

### Assignment inside if condition

### Tuple assignment

### go

## Other

### init

### Buffered Channels

### log.Fatalf
