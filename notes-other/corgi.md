# Corgi

Corgi is a programming language

+ compiled
+ powerful static typing with generics, atoms, and more
+ side-effects tracking
+ exceptions because we have side-effects tracking and value our time
+ design by contract with partial evaluation at compile time
+ mutability instead of pointers
+ huge stdlib
+ small set of conceptions
+ clean syntax with words instead of symbols
+ type inference and implicit type casting
+ friendly grammar, strict linter, helpful formatter.

## Atoms

```
atom True
atom False
```

## Custom Types

```
# set of values or atoms
type Bool = True or False

# type alias
type Answer = Bool

# struct
type Just(T)
  # any one capital letter states for generic type
  value T

# union of type and value
atom Nothing
type Maybe = Just or Nothing
```

Type casting:

```
# cast
ok = Bool(True)
answ = Answer(ok)
```

It is optional since we have type inference but still useful to have stricter types.

## Built-in Types

```
# std.Int
12

# std.Float
12.0
0.1

# std.Str
"abc"

# std.Chan
```

All other types can be constructed from it.

A few useful functions:

```
import "int"
import "str"

int.from_hex("F1")
str.unescape("\n")
```

## Functions

```
import "std"

func fib
  # type is optional, type inference is a thing
  public n std.Int
  if n <= 1
    return 1
  return fib(n-1) + fib(n-2)
```

## Constants

Any globally defined value is a constant. Constant can be either Int, Float, Str, or atom

```
PI = 3.1415
```

## Default values

Default value can be only a constant

```
DEFAULT_STEP = 1

type Range
  start = 0
  end
  step = DEFAULT_STEP

r = Range(start=1, end=10)

# default value for a func arg
func fib
  public n = 2
```

## Enums

Any type field default value can be accessed without creating an instance. You can use it for enums:

```
Color = std.Str
type Colors
  red = Color(1)
  green = Color(2)
  blue = Color(3)

Colors.red # 1
```

## Methods

```
type Count
  start = 0

  func count.next
    return count.start + 1

c = Count(start=1)
c.next() # 2
```

## Calling things

Funcs:

```
# without passing arguments
user.activate()

# func with only one argument (including with default values)
int.from_hex("F1")
```

Variadic arguments:

```
func slice
  public values...
  return None

slice(1, 2, 3)
```

## Conditions and cycles

```
if user.is_active()
  ...

while user.is_active()
  ...

for i in std.Range(stop=10)
  ...
```

## Concurrency

Golang concurrency is nice and powerful:

```
type Range
  start = 0
  end
  step = 1

  func range.iter
    mutable ch = std.Chan(size=1, T=std.Int)
    func do
      current = range.start
      while current < range.end
        ch.send(current)
        current += 1
    spawn do
    return ch
```

`for` cycle calls `.iter` method from the given object and iterates over the result. Iteration happens by calling `.next` method. The simplest way to define iterator is with channels as shown above.

## Mutability

Pointers management is done by compiler. Humans use mutability conception instead. Everything is immutable by default. If you want to call a method or function that mutates an object, you must create the object with `mut` keyword:

```
type Chan(T)
  size std.Int

  mut func chan.send
    public value T
    ...

# ok
mut ch = Chan(size=1, T=std.Int)
ch.send(1)

# compile error
ch = Chan(size=1, T=std.Int)
ch.send(1)
```

## Markers

Markers is a way to track side-effects:

```
mark io
func print
  public value std.Str
  ...

# ok
func main
  print(1)

# ok
mark io
func main
  print(1)

# ok
mark io, no raises
func main
  print(1)

# compile error
mark no io, no raises
func main
  print(1)
```

You can use any markers you wish. Stdlib funcs has `io`, `network`, and `raises`.

## Exceptions

Yes, we have exceptions. "Let it crash". Exceptions are tracked by markers mechanism.

```
func divide
  raise ZeroDivisionError


# ok
mark raises(ZeroDivisionError)
func divide
  raise ZeroDivisionError

# compile error
mark raises(ValueError)
func divide
  raise ZeroDivisionError

# compile error
mark raises(ZeroDivisionError, ValueError)
func divide
  raise ZeroDivisionError

# compile error
mark no raises
func divide
  raise ZeroDivisionError
```

Specify markers for caller func to have control over it:

```
# ok
func main
  divide()

# ok
mark raises(ZeroDivisionError)
func main
  divide()

# compile error
mark no raises
func main
  divide()

# compile error
mark raises(ValueError, AnotherError)
func main
  divide()
```

Catch in Python style:

```
try
  raise SomeError
catch SomeError as error
  std.print("panic!")
  raise error
```

## Asserts

When it is possible, `assert` will be checked on partial evaluation stage at compile time:

```
func divide
  public value std.Float
  public on std.Float
  assert on != 0
  ...

func main
  # compile error
  divide(value=13, on=0)
```

## Pattern matching

You can match a pattern on strings with globs:

```
import int
import std

match int.to_str(13)
  "?"
    std.print("less than 10")
  "1?"
    std.print("between 10 and 20")
  "-*"
    std.print("negative")
  "*"
    std.print("20 or more")
```
