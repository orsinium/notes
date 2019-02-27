# How to work with date and time in Go

## Standard library

Ok, there is how you can parse and format date or time string into `time.Time` object:

```go
t = time.Parse(format, timeString)
t.Format(format)
```

And this format is the most strange thing in Go. There is example of format:

```
Mon, 02 Jan 2006 15:04:05 -0700
```

My first thought was "Wow, amazing, smart Go can get example of string as format". No. If you pass "2007" instead of "2006" your program will fail in runtime. It has to be exactly the same values as in the example above.

Luckily, Go has some constants for different time standards. For example, `UnixDate`, `RFC822`, `RFC3339`.

## Parsers

+ [dateparse](https://github.com/araddon/dateparse) -- parse date or time in unknown format. Can understand really much formats, from US and Chinese formats to UNIX timestamp.
+ [when](https://github.com/olebedev/when) -- a natural language date and time parser. Has rules for English and Russian.

## Formatters

Let's write `2006-01-2` with different formats.

+ [jodaTime](https://github.com/vjeantet/jodaTime) -- parse or format time with [yoda syntax](http://joda-time.sourceforge.net/apidocs/org/joda/time/format/DateTimeFormat.html). For example, `YYYY-MM-d`.
+ [strftime](https://github.com/awoodbeck/strftime) -- format time with [C99 syntax](https://en.cppreference.com/w/c/chrono/strftime). For example, `%Y-%m-%d`.
+ [tuesday](https://github.com/osteele/tuesday) -- format time with [Ruby syntax](https://ruby-doc.org/core-2.4.1/Time.html#method-i-strftime). For example, `%Y-%m-%-d`.

And bonus:

+ [durafmt](https://github.com/hako/durafmt) -- format duration to string like "2 weeks 18 hours 22 minutes 3 seconds".

## Helpers

+ [now](https://github.com/jinzhu/now) -- set of functions to calculate time based on another time. For example, `now.New(t).BeginningOfMonth()` returns first second of month in moment of `t`.
+ [timeutil](https://github.com/leekchan/timeutil) -- contains `timedelta` like in Python and some operations with time.
