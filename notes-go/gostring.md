# How yo use GoString in Go

The package [fmt](https://pkg.go.dev/fmt) defines [GoStringer](https://pkg.go.dev/fmt#GoStringer) interface with the following documentation:

> GoStringer is implemented by any value that has a GoString method, which defines the Go syntax for that value. The GoString method is used to print values passed as an operand to a %#v format.

What that means is that you can implement `GoString() string` method on any of your types, and it will be called when the object of this type is formatted using `%#v`. And the purpose of this is to return a representation of the object in Go-syntax.

## Example

The [errors.New](https://pkg.go.dev/errors#New) returns an `error`. But since `error` is just an interface, it, in fact, returns a private struct that satisfies the interface. And indeed, if we print the result with `%#v` flag, we'll see this struct, including all private fields:

```go
func main() {
    e := errors.New("oh no")
    fmt.Printf("%#v", e)
    // Output: &errors.errorString{s:"oh no"}
}
```

And this is the relevant source code of the package:

```go
func New(text string) error {
    return &errorString{text}
}

type errorString struct{ s string }

func (e *errorString) Error() string {
    return e.s
}
```

We can make it better. Let's copy-paste this source code and add to the struct one more method:

```go
func (e *errorString) GoString() string {
    return fmt.Sprintf(`errors.New(%#v)`, e.s)
}
```

And if we print it now, we'll see a nice and clean output of our new method:

```go
func main() {
    e := New("oh no")
    fmt.Printf("%#v", e)
    // Output: errors.New("oh no")
}
```

## Why

The idea isn't new. For instance, Python has [repr](https://docs.python.org/3/library/functions.html#repr) function the output of which can be customized by adding [`__repr__`](https://docs.python.org/3/reference/datamodel.html#object.__repr__) method to a class. The only difference is that Python stdlib actively uses this method to make the output friendly. For example:

```python
import datetime
d = datetime.date(1977, 12, 15)
print(repr(d))
# Output: datetime.date(1977, 12, 15)
```

It gives several benefits:

+ It hides internal implementation from the user.
+ It looks cleaner.
+ It allows the user to copy-paste the output and (assuming all required imports are in place) get the object created. It can be helpful, for instance, to hardcode values for tests.

## Go built-ins

Built-in types give good enough output:

```go
m := map[string]int{"hello": 42}
fmt.Printf("%#v", m)
// map[string]int{"hello":42}

b := []byte("hello")
fmt.Printf("%#v", b)
// []byte{0x68, 0x65, 0x6c, 0x6c, 0x6f}
```

And if you want a bit nicer output, have a look at [dd](https://github.com/Code-Hex/dd) package which is designed exactly for the purpose of printing structs and built-in types in a nice Go syntax:

```go
fmt.Println(dd.Dump(m))
// map[string]int{
//   "hello": 42,
// }
```

## Go stdlib

The stdlib does use it in a few places but most of the time it doesn't. We've already seen the output of `errors.New`. Let's see some more examples.

✅ `time.Date`:

```go
v := time.Unix(0, 0)
fmt.Printf("%#v", v)
// time.Date(1970, time.January, 1, 1, 0, 0, 0, time.Local)
```

❌ `fmt.Errorf`:

```go
e := errors.New("damn")
v := fmt.Errorf("oh no: %w", e)
fmt.Printf("%#v", v)
// &fmt.wrapError{msg:"oh no: damn", err:(*errors.errorString)(0xc000010250)}
```

❌ `sync.WaitGroup`:

```go
v := sync.WaitGroup{}
fmt.Printf("%#v", v)
// sync.WaitGroup{noCopy:sync.noCopy{}, state1:0x0, state2:0x0}
```

❌ `list.New`:

```go
v := list.New()
fmt.Printf("%#v", v)
// &list.List{root:list.Element{next:(*list.Element)(0xc00007e150), prev:(*list.Element)(0xc00007e150), list:(*list.List)(nil), Value:interface {}(nil)}, len:0}
```

## PSA

I want you to know that if stdlib doesn't do something, it doesn't matter you shouldn't. `GoString` doesn't worth bothering in your internal projects, but if you develop an open-source package, please, spend a few seconds of your life and make this representation of each of your types a little bit more useful.
