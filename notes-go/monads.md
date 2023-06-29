# In search of better error handling for Go

This article is an exploration of how to improve error handling in Go. I address here some of the issues while others are left with open questions and some ideas. And, spoiler alert, I do love error handling in Go as it is now. I don't want to replace it with anything like exceptions, but I want to make it slightly better.

I'm going to limit all solutions to what we already have in the language. I'm not talking about any language changes or making a new programming language out of Go. Everything we do here must be possible to shape into a ready-to-use pure Go package.

## How error-handling in Go works

If you already know Go, skip to the next section.

In Go, you can return multiple values from a function:

```go
func split(s string) (string, string) {
    return "left", "right"
}
```

It looks like something other languages call "tuple," but in Go, there is no such type you can operate on. Instead, these are two separate values returned.

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

Note that you always need to return something as the first value, even if there is an error. The convention is to return the default value for the type: nil for pointers, 0 for integers, an empty string for strings, etc.

In functions that call a function returning an error, you should explicitly check for an error and propagate it to the caller:

```go
func createUser() (*User, error) {
    conn, err := connect()
    if err != nil {
        return nil, err
    }
    ...
}
```

And at the very top or when applicable, you may handle the error somehow. For example, log it or show it to the user:

```go
func main() {
    user, err := createUser()
    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}
```

It might be hard to find in that way where the error occurred (imagine that we call `connect` in 10 different places), so the best practice (available since Go 1.13) is to wrap each error before returning it:

```go
if err != nil {
    return nil, fmt.Errorf("connect to database: %v", err)
}
```

You can think of it as building a stack trace manually.

Another option for error handling is to raise them using `panic`. The panic will include the stack trace, and you can provide it with an error message to be shown. However, Go doesn't have `try/catch`, so handling such errors is hard. You may `defer` a function to be executed when leaving the current function scope. This inner function will be called even if a panic occurs, and it can call the `recover` function to stop the panic, get the panic value, and act on it somehow.

Using `panic` and `recover` is convoluted and dangerous. The `panic` is usually used for errors that shouldn't occur, and `recover` is reserved for the entry point level code, like the web framework, so you won't see it often.

## Why it's cool

The Go error handling gets a lot of criticism for being verbose and tedious to write. However, it often pays back:

1. It's **user-friendly**. When you write a CLI application for a general audience, in case of failure, you want to show a friendly and clean error message instead of a big scary traceback that makes sense only for people who know exactly how the tool works. And in Go, by design, each possible error is manually crafted to be human-readable and friendly.
1. It's **explicit**. In languages with exceptions, the function execution can be interrupted at any point, and you have to always keep it in mind. In Go, the function returns only when you explicitly write `return` (if you don't count `panic`). That makes it always apparent at first glance which lines of code and in which scenarios might be skipped.

Both exceptions and explicit error handling have their advantages and disadvantages, and programming languages usually pick one of the two, depending on their goals and application. Go is designed to be simple and explicit, even if often verbose, so here we have it. Erlang and Elixir have both types of errors, which allows for more advanced error handling and for picking what fits a specific task the best, but that has a higher learning curve and requires making a conscious choice of what should be used in each particular situation.

## What's the problem

I think verbosity and repetitivity are often worthy sacrifices to make for the benefits described above, and I think it fits the Go design goals quite well. No, the main problem I see is that **it's possible and easy not to handle errors**. While exceptions will always propagate and explode if not handled explicitly, unhandled errors in Go are simply discarded. Let's look at a few examples:

```go
createUser()
```

Here we called a function that may return an error, but we didn't check for it. It's also possible that when we were writing this code, `createUser` didn't return an error. Then we updated it to return one, but we forgot to check all places where it is called and add error handling explicitly.

There is a linter to catch such scenarios called [errcheck](https://github.com/kisielk/errcheck), and you should certainly use it. However, linters aren't code verifiers or type checkers, and there are scenarios when they might miss something.

Also, errcheck allows you to explicitly discard errors, like so:

```go
user, _ := createUser()
```

Or like this when the function returns only an `error` without a value:

```go
_ = something()
```

You may see it in the following scenarios:

1. The author **assumes that the error may never happen**. In this scenario, it would be much better to `panic` if the assumption is wrong, but explicitly checking for the error and panicking is, as with all error handling in Go, tedious and verbose, and people don't want to do that for errors that "won't ever happen anyway."
1. The author **doesn't know what to do with the error**. For example, if we cannot write a message in the log file. In that scenario, we can't log the error because the error is about the logger not working (and we'll get into an infinite loop). And we can't panic because a (probably temporary) issue with the logger (which isn't business-critical) doesn't worth breaking everything.
1. The author **copy-pasted an example from the documentation**. Documentation authors often skip error handling to keep examples simple, and people often copy-paste these examples but forget to adjust them.

So, this is what we'll try to fix. Let's try to find a way to force people to check for errors before they can work with the function return value.

## Fixing unintentionally silent errors

The [regexp.Compile](https://pkg.go.dev/regexp#Compile) function compiles the given regular expression and returns a pair `(*Regexp, error)`:

```go
var rex, _ = regexp.Compile(`[0-9]+`)
```

Most often, regexes are compiled at the module level at the start of the application so that when it comes to actually using the regex, it is fast. So, that means we don't have a place to propagate the error. And we don't want to ignore the error, or it will explode with a nil pointer error when we try using the regex. So, the only option left is to panic. It works quite well there because since we compile a hardcoded regex and do that at the start of the application, we know for sure it won't panic when we test it and ship it to users or production.

And since this is such a common scenario, the `regexp` module provides [regexp.MustCompile](https://pkg.go.dev/regexp#MustCompile) function that does the same but panics on error instead of returning it. Here is how it looks inside:

```go
func MustCompile(str string) *Regexp {
    regexp, err := Compile(str)
    if err != nil {
        panic(`regexp: Compile(` + quote(str) + `): ` + err.Error())
    }
    return regexp
}
```

Writing such a wrapper for every single function in the project doesn't scale well. But, thanks to generics, we can make a generic version of the wrapper that works with any function:

```go
func Must[T any](val T, err error) T {
    if err != nil {
        panic(err)
    }
    return val
}
```

And that's how we can use it:

```go
var rex = Must(regexp.Compile(`[0-9]+`))
```

This is one of the error-handling functions I provide in [genesis](https://github.com/life4/genesis) (the library with generic functions for Go): [lambdas.Must](https://pkg.go.dev/github.com/life4/genesis/lambdas#Must).

That solves the problem of handling errors that must never occur but which we don't want to silently discard. Now, let's see how we can ensure that regular errors are properly handled.

## Meet monads

"Monad" is just a fancy word for "container" or "wrapper". For example, a linked list is a monad that wraps values inside and provides functions like `map` to interact with these values.

The monad we're interested in today in Rust is called `Result` and in Scala is called `Try`. We'll use the Rust naming here. This monad wraps either the function result or an error. In Go, we can use the power of interfaces for that:

```go
type Result[T any] interface {
    IsErr() bool
    Unwrap() T
    ErrUnwrap() error
}
```

The successful result will be represented by a private struct `ok` constructed with the `Ok` function:

```go
type ok[T any] struct{ val T }

func Ok[T any](val T) Result[T] {
    return ok[T]{val}
}

func (r ok[T]) IsErr() bool      { return false }
func (r ok[T]) Unwrap() T        { return r.val }
func (r ok[T]) ErrUnwrap() error { panic("expected error") }
```

```go
type err[T any] struct{ val error }

func Err[T any](val error) Result[T] {
    return err[T]{val}
}

func (r err[T]) IsErr() bool      { return true }
func (r err[T]) Unwrap() T        { panic(r.val) }
func (r err[T]) ErrUnwrap() error { return r.val }
```

Now, let's take the code from the intro and rewrite it.

Classic Go:

```go
func connect() (*Connection, error) {
    return nil, errors.New("cannot connect")
}

func createUser() (*User, error) {
    conn, err := connect()
    if err != nil {
        return nil, err
    }
    return &User{conn}, nil
}
```

And now with monads:

```go
func createUser() Result[User] {
    res := connect()
    if res.IsErr() {
        return Err[User](res.ErrUnwrap())
    }
    conn := res.Unwrap()
    return Ok[User](User{conn})
}
```

There are a few things that can be slightly improved by adding a few more methods:

1. The `ErrAs` method may be added to convert the type for an error (and panic if it's not an error). So, `Err[User](res.ErrUnwrap())` can be replaced by `res.ErrAs[User]()`.
1. The `Errorf` method may be added to format the wrapped error with `fmt.Errorf` (and do nothing if it's not an error).

But these are details.

The good thing about the monadic approach is that it's impossible to use the returned value if an error occurs. The `Unwrap` method will panic if you forget to check for errors first. The bad thing about it is that it's still possible to forget to check for errors; the only difference is that it will panic instead of going unnoticed. And we don't want our code to panic. And if the error doesn't occur often enough and is not covered by tests (which is almost always the case), that panic is hard to notice until it hits the production.

And also, it's even more verbose.

Can we do better than that?

## Try

Let's talk about [the most disliked](https://github.com/golang/go/issues?q=is%3Aissue+sort%3Areactions--1-desc+is%3Aclosed) Go proposal: [A built-in Go error check function, `try`](https://github.com/golang/go/issues/32437). That's exactly how error handling works in Rust. There is a `Result` monad and a `?` postfix operator (before that, Rust also used to have a `try` macro) that propagates the error. With the proposal accepted, our code would look like this:

```go
func createUser() (*User, error) {
    conn := try(connect())
    return &User{conn}, nil
}
```

It is short, it ensures that the error is not ignored, and it ensures that the value is not used if there is an error. So, why the proposal got so much negativity?

1. **It was solving the wrong problem**. At the time the proposal was made (Go 1.12), the language didn't have error wrapping. And this proposal is what motivated the Go team to add `fmt.Errorf` in the very next release.
1. **It wasn't well-communicated**. The proposal was introduced out of the blue by the Go team together with a proposal for contract-based generics, and many people perceived it as an already-made decision. There were many blog posts and comments in the community that Go is a Google language and that whatever we all think doesn't matter. Rejecting both proposals was the best decision by the Go team to not let the community fall apart.
1. **It didn't address error-wrapping**. It was suggesting to use `defer` to wrap errors. But this point isn't hard to fix. We can just let `try` to accept as the second argument the format string to format the error.
1. **It's one more way to interrupt the control flow**. There are a few keywords (`break`, `continue`, `return`, and the infamous `goto`) and one function (`panic`) that might interrupt the regular function flow, and adding one more function in the mix would make reading code harder.

These are certainly valid points, but considering that this is how error-handling is designed in Rust and that people there love it, I'd say it doesn't deserve all the hate it gets, and having it properly presented now would go differently.

Regardless, can we add something like this ourselves? Well, not exactly. The only way to interrupt function control flow from another function is with `panic`. But if we want to stop the error propagation, we need to `defer` a function that will `recover` after the panic:

```go
func createUser() (u *User, err error) {
    defer func(){err = DontPanic()}()
    ...
}
```

And now we have the same problem as we had before: if you forget to add this line in a function, instead of an error, you'll get panic.

## Type guards

Let's look again at the first example we have of handling errors with monads:

```go
res := connect()
if res.IsErr() {
    return Err[User](res.ErrUnwrap())
}
conn := res.Unwrap()
```

The problem here is that if we look at the code, we know that inside of the `if` block, `res` has a type `err`. And since we always return from this block and there are only 2 types that implement `Result`, after this check, the `res` might be only `ok`. Can we explain it to the type checker? Then we could define safe-to-use methods that are available on the refined types but not on the `Result`:

```go
func (r ok[T]) Val() T      { return r.val }
func (r err[T]) Val() error { return r.val }
```

In Python, we could use [typing.TypeGuard](https://docs.python.org/3/library/typing.html#typing.TypeGuard) to refine the type. So, our code would look something like this:

```python
class Result(Protocol):
    def is_err(self) -> TypeGuard[Err]:
        pass
```

But in Go, the only way to refine a type is to explicitly use [type switches](https://go.dev/tour/methods/16):

```go
var conn Connection
switch res := connect().(type) {
case ok[Connection]:
    conn = res.Val()
case err[Connection]:
    return Err[User](res.Val())
}
```

That's quite similar to what you could do in Rust:

```rust
let conn = match connect() {
    case Ok(val) => val,
    case Err(err) => return Err(err),
}
```

With this approach, we are guaranteed to never get panic and only be able to unwrap the value if we check the type of the container. However, there is no "exhaustiveness check" for the `switch` statement in Go. The compiler won't tell us anything if we don't check for `ok` or for `err`. It also won't tell if we forgot to assign the unwrapped value to `conn`. In all these scenarios, we at the end get `conn` with the default value, which is the same result we get when we ignore the error in the classic approach, except now it's much more verbose.

## Piping

In Haskell, there are also no exceptions. But also, there is no `return`. To deal with errors, you only have monads. But these monads are powerful enough to deal with any kind of error in a very concise way. How does Haskell do that?

First, meet the monad `Maybe`. It can be either `Just` containing a value or `Nothing`, which is equivalent to `nil` in Go (or `None`, or `null`, or something like this in other languages). Here is how it is defined:

```haskell
data Maybe a = Just a | Nothing
```

Now, let's make a few functions:

```haskell
data User a = User a deriving Show

connect = Nothing
user_from_conn conn = Just(User(conn))
validate_user user = Just(user)

create_user = connect >>= user_from_conn >>= validate_user
```

The operator `>>=` is where the magic happens. First, it evaluates the value on the left. If it is `Just a`, it extracts the value `a` from it and calls with it the function on the right. If the value on the left is `Nothing`, the operator doesn't call the right function, and `Nothing` is simply returned.

If you call `create_user` on the code above, `connect` will return `Nothing`, so `user_from_conn` and `validate_user` aren't even called, and the function result will be `Nothing`.

Here is a better example that shows how it works:

```haskell
-- returns Just the given value divided by 2 if the value is even,
-- and Nothing otherwise
half x = if even x then Just (x `div` 2) else Nothing

Just 3 >>= half     -- returns `Nothing`
Just 4 >>= half     -- returns `Just 2`
Nothing >>= half    -- returns `Nothing` without even calling `half`
```

The operator `>>=` is so important that it is Haskell's logo. And since using it is so common, Haskell also provides a convenient syntax sugar for piping together multiple function calls:

```haskell
create_user = do
    conn <- connect
    user <- user_from_conn conn
    validate_user user
```

If you want to dive deeper, the blog post [Functors, Applicatives, And Monads In Pictures](https://www.adit.io/posts/2013-04-17-functors,_applicatives,_and_monads_in_pictures.html) has more nice examples of defining and using monads in Haskell.

Elixir doesn't use the word "monad", but it has a very similar syntax for doing about the same thing:

```elixir
with {:ok, conn} <- connect(),
     # This line is executed only if the previous line matched
     {:ok, user} <- user_from_conn(conn)
     {:ok, user} <- validate_user(user)
do
  # This line is executed only if all lines above matched
  user
else
  # This line is executed if any of the `with` matches failed
  err -> err
end
```

Can we do something similar in Go?

```go
Pipe(
    connect,
    createUser,
    validateUser,
)
```

Well, kinda. There is no type-safe way to implement this function. We could write something like this:

```go
func Pipe[T any](funcs ...func(T) Result[T]) Result[T] {
    ...
}
```

But that will require all functions to accept and return the same type. It won't even work with our example where the first function returns `Connection`, and the next one returns `User`. To solve it, we could make a separate function for each number of possible arguments:

```go
func Pipe2[T1, T2, T3 any](
    f1 func(T1) Result[T2],
    f2 func(T2) Result[T3],
) Result[T3] {
    return Err[T](errors.New(""))
}
```

We could live with that, that's already something. But then we have a problem that all the functions now accept exactly one argument. What if we want to pass an additional argument to one of these functions? We could wrap it in a new anonymous function just for this purpose, but that's, again, very verbose.

## Flat map

There are a few methods that the monad has to work with the wrapped value:

+ `FMap` (aka `flatMap` or `and_then`) applies the given function to the `Result` and returns the `Result` of that function.
+ `Map` applies the given function to the Result and returns the wrapped in `Ok` result of that function.

And it's quite easy to implement them:

```go
type Result[T any] interface {
    // ...
    FMap(func(T) Result[T]) Result[T]
    Map(func(T) T) Result[T]
}

func (r ok[T])  FMap(f func(T) Result[T]) Result[T] { return f(r.val) }
func (r ok[T])  Map(f func(T) T)          Result[T] { return Ok(f(r.val)) }
func (r err[T]) FMap(func(T) Result[T])   Result[T] { return r }
func (r err[T]) Map(func(T) T)            Result[T] { return r }
```

And that's how we could use it:

```go
// THIS CODE DOES NOT COMPILE
func createUser() Result[User] {
    return connect().Map(
        func(conn Connection) User {
            return User{}
        },
    )
}
```

This code doesn't compile. The reason is that the signature of the methods requires the function passed into `Map` or `FMap` to return the same (wrapped) type as of the current monad. That would work if we'd accept and return `Connection`, but since we return `User`, the compilation fails.

The current implementation of generics [does not permit parametrized methods](https://go.googlesource.com/proposal/+/refs/heads/master/design/43651-type-parameters.md#No-parameterized-methods). You can track the progress of the feature in the proposal: [allow type parameters in methods](https://github.com/golang/go/issues/49085). But for now, all we can do is make `Map` and `FMap` functions:

```go
func Map[T, R any](r Result[T], f func(T) R) Result[R] {
    //Implementation is left as an exercise for the reader
}

func FMap[T, R any](r Result[T], f func(T) Result[R]) Result[R] {
    //Implementation is left as an exercise for the reader
}
```

And that's how we can use it:

```go
func createUser() Result[User] {
    return Map(
        connect(),
        func(conn Connection) User {
            return User{conn}
        },
    )
}
```

That works quite well, especially if each step of the algorithm is a function. You'd need to keep assigning each result to a variable, though, to avoid crazy nesting. For example:

```go
key := openssl.GenerateRSAKey(2048)
pubKey := FMap(key, MarshalPKIXPublicKeyPEM)
return FMap(pubKey, Armor)
```

But in practice, that's a rare situation. You'll often face situations when you need to call a method instead of a function, pass additional parameters, or do something with 2 or more results. In all such cases, you'll need to wrap the operation into an anonymous function that provides the signature expected by `FMap`. And there are 2 problems with it:

First, **bad performance**. Each function needs a stack, and now each line of code defines an anonymous function. I don't know how good the compiler is at inlining this stuff and how much exactly it might affect the performance, but it's worth keeping in mind.

And second, **verbose syntax**. That's where we get to the most disliked open proposal (this blog post walks a dangerous path of controversy): [Lightweight anonymous function syntax](https://github.com/golang/go/issues/21498). Without it, each call to `FMap` is a chore to type and a mess to read.

Compare the same example in (semi-)functional languages and in Go:

Rust:

```rust
|a, b| { a + b }
```

Haskell:

```haskell
(+)
```

Elixir:

```elixir
&(&1 + &2)
```

Go:

```go
func(a int, b int) int { return a + b}
```

This is one of the small things that seem not important but are crucial for a language to be functional.

## The best solution

If I could shape Go to my will, I think the best solution would be to have a `Try` method on the `Result` monad that behaves pretty much like the rejected `try` proposal. However, I don't see a way to do that with the means currently available in the language, and I don't see it possible to get a proposal for it merged in the language. So, this blog post currently has more questions than answers.

There are many projects that simply copy monads from other languages (the most famous one being [mo](https://github.com/samber/mo)), but I don't think it works well in the current state of Go because of all the reasons described above. However, things might change if any of these proposals (or their variation) is accepted:

+ [Add sum types / discriminated unions](https://github.com/golang/go/issues/19412)
+ [Add typed enum support](https://github.com/golang/go/issues/19814)
+ [Allow type parameters in methods](https://github.com/golang/go/issues/49085)
+ [Lightweight anonymous function syntax](https://github.com/golang/go/issues/21498)
+ [A built-in Go error check function](https://github.com/golang/go/issues/32437)

Until then, I don't see user-implemented monads as a good fit for Go.

## What can you already use

There are a few small things in this blog post that you can already bring on the production and make your code safer:

+ The [errcheck](https://github.com/kisielk/errcheck) linter is a must-have for any Go project. If you don't already use it, please do. The [golangci-lint](https://golangci-lint.run/) aggregator supports it out of the box and runs by default.
+ The `Must` function. You can copy-paste it from [genesis](https://github.com/life4/genesis/blob/v1.2.0/lambdas/errors.go). I hope one day, something similar will be added to the stdlib. Use it instead of discarding an error in every place where an error can "never" occur. Because when it does occur, you'd better know about it.
+ Always include error handling in all code examples and documentation. That way, when people copy-paste it into their project, they don't forget to handle errors properly.
