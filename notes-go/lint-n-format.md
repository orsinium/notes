# Go linters and formatters

## Linters

The first linter you face coming into Go is [go vet](https://golang.org/cmd/vet/). This is a built-in linter targeted mostly on finding bugs rather than code style.

Another official linter from the Go core team is [golint](https://github.com/golang/lint). This one is targeted on finding not bugs but only style issues from the official [code review guide](https://github.com/golang/go/wiki/CodeReviewComments) and [effective go](https://golang.org/doc/effective_go.html).

If you want catch more bugs and write more effective code, consider running more linters. Go has plenty of them. Of course, it would be hard to download, install, and run all of them. Luckily, we have an amazing [golangci-lint](https://golangci-lint.run/). This is a wrapper, providing a single unified way to run and configure [more than 40 linters](https://golangci-lint.run/usage/linters/). Keep in mind that by default it runs only a few of them, so it's good to have an explicit configuration with listing of all linters you want to use in the project. And if you want to see from what you can start, below are some most notable linters.

A few biggest linters:

+ [staticcheck](https://staticcheck.io/docs/) has a huge collection of checks, target on finding bug, improving code readability and performance, simplifying code.
+ [go-critic](https://go-critic.github.io/) has also many different checks of all kinds: bugs, performance, style issues. It is positioned as "the most opinionated linter", so, probably, you want to disable a few checks but only a few. Don't ask what's better, staticcheck or go-critic, just use both.
+ [gosec](https://github.com/securego/gosec) is targeted exclusively on finding security issues.


A few more specific but helpful linters:

+ [errcheck](https://github.com/kisielk/errcheck) finds errors that you forgot to check. [Always check all errors](https://github.com/golang/go/wiki/CodeReviewComments#handle-errors) and do something meaningful, don't let them pass unnoticed.
+ [ineffassign](https://github.com/gordonklaus/ineffassign) finds an assignment that has no effect. In most of the cases, it happens when you assigned an error into previously created `err` variable but forgot to check it.

Useful linters without golangci-lint integration (yet?):

+ [revive](https://github.com/mgechev/revive) is a stricter and faster alternative to golint with a lot of rules. Most of the rules are about code style and consistency, some are opinionated. No need to worry, the linter allows to configure or disable any check.
+ [sqlvet](https://github.com/houqp/sqlvet) lints SQL quearies in Go code for syntax errors and unsafe constructions.
+ [semgrep-go](https://github.com/dgryski/semgrep-go) finds simple bugs.

What should you use? Everything you can! If you have an existing project, enable all linters that are easy to integrate, and then slowly, one by one, try and enable all that look reasonable and helpful. Just give it a try! Also, be mindful of your coworkers, help them to fix a code that a lintert complains about, and be ready to disable a check if it works not so well for your codebase, especially if it is only about a code style.

Further reading:

+ [awesome-go-linters](https://github.com/golangci/awesome-go-linters)
+ [golangci-lint supported linters](https://golangci-lint.run/usage/linters/)

## Formatters

One of the most famous go features is a built-in code formatter [gofmt](https://golang.org/cmd/gofmt/). Gofmt is your friend, use gofmt. There is no specification about what exactly gofmt does because the code evolves and changes rapidly, fixing formatting bugs and corner cases.

...

## Custom rules

If you have a custom rule you'd like to validate or reformat in your project, there are few linters and tools that can be helpful:

+ [gomodguard](https://github.com/ryancurrah/gomodguard) allows to forbid usage of particular modules or domains.
+ [ruleguard](https://github.com/quasilyte/go-ruleguard) is not actually a linter at the moment but a framework for fast writing of simple rules. It has a [custom DSL](https://github.com/quasilyte/go-ruleguard/blob/master/docs/gorules.md) that can be used to lint code as well as rewrite specific constructions. It [can be integrated](https://quasilyte.dev/blog/post/ruleguard/#using-from-the-golangci-lint) with golangci-lint via go-critic.

## Integrations

+ [Golangci-lint has integrations with everything](https://golangci-lint.run/usage/integrations/).
+ [Gofumpt has integration with VSCode and a guide for GoLand](https://github.com/mvdan/gofumpt#installation).
