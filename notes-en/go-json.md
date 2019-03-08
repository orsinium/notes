# Work with JSON from Go and command line

## Go standard library

In Go creating of the JSON quite simple, just pass any data in `json.Marshal`, and you get the bytes with JSON. But parsing of JSON is painful, especially when you want only one field that located very deep in the source JSON. You have to create all maps and structs for all places where located fields that you need. See full example on [Go by Example](https://gobyexample.com/json).

## Make it better

+ [gjson](https://github.com/tidwall/gjson) -- allows you to get any data from JSON very simple, without difficult conversions and type-casting. For example, how you can get `lastName` from all objects in the `programmers` field: `gjson.Get(json, "programmers.#.lastName").Array()`. Beautiful!
+ [sjson](https://github.com/tidwall/sjson) -- same thing for setting up values in the JSON data: `sjson.Set(json, "name.last", "Anderson")`.

## Command line

+ [jj](https://github.com/tidwall/jj) -- CLI around `gjson` and `sjson` for getting and editing values in JSON stream.
+ [jd](https://github.com/tidwall/jd) -- same as `jj`, but interactive. Really useful tool for constructing paths for `gjson`.
+ [jq](https://stedolan.github.io/jq/tutorial/) -- like `jj`, but with beautify, syntax highlighting, simple installation from repos and alternative syntax. This is really powerful tool with regexp, functions, many arguments, variables, Turing complete language.

You can beautify output of any command that writes JSON logs to stdout just piping it to `jq`:

```json
$ go run tmp.go | jq
{
  "level": "info",
  "message": "hello world!"
}
{
  "level": "info",
  "message": "hello again",
  "testInt": 0
}
```

However, `jq` fails if input contains non-JSON lines. I don't know how to fix it. I've found [isuue](https://github.com/stedolan/jq/issues/682) where authors recommend to use `--seq` key for it, but it doesn't work for me. So, in this case you can use [bat](https://github.com/sharkdp/bat) -- clone of [cat](https://bit.ly/2NMm67N) with syntax highlighting, lines numbering, pagination and git support.

```json
go run tmp.go | bat -l jsonnet
───────┬──────────────────────────────────────────────────────
       │ STDIN
───────┼──────────────────────────────────────────────────────
   1   │ broke
   2   │ {"level":"info","message":"hello world!"}
   3   │ broke again
   4   │ {"level":"info","message":"hello again","testInt":0}
```

## Appendix

Code that I used for tests:

```go
package main

import (
	"fmt"
	"os"
	"time"

	"github.com/francoispqt/onelog"
)

func main() {
	fmt.Println("broke")
	logger := onelog.New(os.Stdout, onelog.ALL)
	logger.Info("hello world!")
	fmt.Println("broke again")
	for i := 0; true; i++ {
		time.Sleep(2 * time.Second)
		logger.InfoWith("hello again").Int("testInt", i).Write()
	}
}
```
