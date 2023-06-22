# In search of better error handling for Go

This article is an exploration of how to improve error-handling in Go. I address here some of the issues while others are left with open questions and some ideas. And, spoiler alert, I actually do love error-handling in Go as it is now. I don't want to replace it with anything like exceptions but I want to make it slightly better.

I'm going to limit all solutions to what we already have in the language. I'm not talking about any language changes or making a new programming language out of Go. Everything we do here must be possible to shape into a ready to use pure Go package.

## How error-handling in Go works

If you already know Go, skip to the next section.

In Go, you can return multiple values from a function:

```go
func split(s string) (string, string) {
    return "left", "right"
}
```

It looks like something other languages call "tuple" but in Go, there is no such type you can operate on, these are actually two separate values returned.

You cannot use it as a type anywhere but in the return type:

```go
// syntax error: expected ')', found ','
func split(s (string, string))
```

And you cannot assign it to a single variable:

```go
// error: cannot initialize 1 variables with 2 values
a := split("")
```

You must either assign it to separate variables:

```go
a, b := split("")
```

Or pass it into a function that accepts 2 arguments:

```go
func example(s1 string, s2 string) {}

func main() {
    example(split(""))
}
```

This all is important because that's how error handling in Go works. The convention is to return the error as the last result value from the functions that may fail:

```go
func connect() (*Connection, error) {
    return nil, errors.New("cannot connect")
}
```

Note that you always need to return something as the first value, even if there is an error. The convention is to return the default value for the type: nil for pointers, 0 for integers, empty string for strings etc.

In functions that call a function returning an error, you should explicitly check for error and propagate it to the caller:

```go
func createUser() (*User, error) {
    conn, err := connect()
    if err != nil {
        return nil, err
    }
    ...
}
```

And at the very top or when applicable you may handle the error somehow. For example, log it or show to the user:

```go
func main() {
    user, err := createUser()
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}
```

It might be hard to find that way where the error occured (imagine that we call `connect` in 10 different places), so the best practice (available since Go 1.13) is to wrap each error before returning it:

```go
if err != nil {
    return nil, fmt.Errorf("connect to database: %v", err)
}
```

You can think of it as building a stack trace manually.

Another option for error handling is to raise them using `panic`. The panic will include the stack trace, and you can provide it an error message to be shown. However, Go doesn't have `try/catch`, so handling such errors is hard. You may `defer` a function to be executed when leaving the current function scope. This inner function will be called even if a panic occurs, and it can call `recover` function to stop the panic, get the panic value, and act on it somehow.

Using panic and recover is convoluted and dangerous. The `panic` is usually used for errors that shouldn't occur, and `recover` is reserved for the entry point level code, like the web framework, so you won't see it often.

## Why it's cool

The Go error handling gets a lot of criticizm for being verbose and tedious to write. However, it often pays back:

1. It's **user-friendly**. When you write a CLI application for a general audience, in case of failure you want to show a friendly and clean error message instead of big scary traceback that makes sense only for people who know exactly how the tool works. And in Go, by design, each possible error is manually crafted to be human-readable and friendly.
1. It's **explicit**. In languages with exceptions, the function execution can be interrupted at any point, and you have to always keep it in mind. In Go, the function returns only when you explicitly write `return` (if you don't count `panic`). That makes it always apparent at the first glance which lines of code and in which scenarios might be skipped.

Both exceptions and explicit error handling have their advantages and disadvantages, and programming languages usually pick one of the two, depending on their goals and application. Go is designed to be simple and explicit, even if often verbose, so here we have it. Erlang and Elixir have both types of errors, which allows for more advanced error handling and for picking what fits a specific task the best, but that has a higher learning curve and requires to make a concious choice what should be used in each particular situation.

## What's the problem

I think verbosity and repetitivity are often worthy sacrifices to make for the benefits described above, and I think it fits the Go design goals quite well. No, the main problem I see is that **it's possible to not handle errors**. While exceptions will always propagate and explode if not handled explicitly, unhandled errors in Go are simply discarded. Let's look at a few examples:

```go
createUser()
```

Here we called a function that may return an error but we didn't check for it. It's also possible that when we were writing this code, `createUser` didn't return an error. Then we updated it to return one, but we forgot to check all places where it is called and add error handling explicitly.

There is a linter to catch such scenarios called [errcheck](https://github.com/kisielk/errcheck), and you should certainly use it. However, linter's aren't code verifiers or type checkers, there are scenarios when it might miss something.

Also, errcheck allows you to explicitly discard errors, like so:

```go
user, _ := createUser()
```

Or like this when the function returns only an `error` without a value:

```go
_ = something()
```

You may see it in the following scenarios:

1. The author **assumes that the error may never happen**. In this scenario, it would be much better to `panic` if the assumption is wrong, but explicitly checking for the error and panicking is, as with all error handling in Go, tedious and verbose, and people don't want to do that for errors that "won't ever happen anyway".
1. The author **doesn't know what to do with the error**. For example, if we cannot write a message in the log file. In that scenario, we can't log the error because the error is about logger not working (and we'll get into an infinite loop). And we can't panic because a (probably temporary) issue with the logger (which isn't business-critical) doesn't worth breaking everything.
1. The author **copy-pasted an example from the documentation**. Documentation authors often skip error handling to keep examples simple, and people often copy-paste these examples but forget to adjust them.

So, this is what we'll try to fix. Let's try to find a way to force people to check for errors before they can work with the function return value.

## Fixing unintentionally silent errors

...

## Meet monads

...
