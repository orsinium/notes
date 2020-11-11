# Go linters and formatters

## Linters

The first linter you face coming into Go is [go vet](https://golang.org/cmd/vet/). This is a built-in linter targeted mostly on finding bugs rather than code style.

Another official linter from the Go core team is [golint](https://github.com/golang/lint). This one is targeted on finding not bugs but only style issues from the official [code review guide](https://github.com/golang/go/wiki/CodeReviewComments) and [effective go](https://golang.org/doc/effective_go.html).

If you want catch more bugs and write more effective code, consider running more linters. Go has plenty of them. Of course, it would be hard to download, install, and run all of them. Luckily, we have an amazing [golangci-lint](https://golangci-lint.run/). This is a wrapper, providing a single unified way to run and configure [more than 40 linters](https://golangci-lint.run/usage/linters/). Keep in mind that by default it runs only a few of them, so it's good to have an explicit configuration with listing of all linters you want to use in the project.

A few biggest linters:

+ [staticcheck](https://staticcheck.io/docs/) has a huge collection of checks, target on finding bug, improving code readability and performance, simplifying code.
+ [go-critic](https://go-critic.github.io/) has also many different checks of all kinds: bugs, performance, style issues. It is positioned as "the most opinionated linter", so, probably, you want to disable a few checks but only a few. Don't ask what's better, staticcheck or go-critic, just use both.
+ [gosec](https://github.com/securego/gosec) is targeted exclusively on finding security issues.

A few more specific but helpful linters:

+ [gosimple](https://github.com/dominikh/go-tools/tree/master/simple) checks for constructions that can be simplified.
+ [errcheck](https://github.com/kisielk/errcheck) finds errors that you forgot to check. [Always check all errors](https://github.com/golang/go/wiki/CodeReviewComments#handle-errors) and do something meaningful, don't let them pass unnoticed.
+ [ineffassign](https://github.com/gordonklaus/ineffassign) finds an assignment that has no effect. In most of the cases, it happens when you assigned an error into previously created `err` variable but forgot to check it.
+ [and much more](https://golangci-lint.run/usage/linters/)

What should you use? Everything you can! If you have an existing project, enable all linters that are easy to integrate, and then slowly, one by one, try and enable all that look reasonable and helpful. Just give it a try! Also, be mindful of your coworkers, help them to fix a code that a lintert complains about, and be ready to disable a check if it works not so well for your codebase, especially if it is only about a code style. And if you want to see from what you can start, below are some most notable linters.

## Formatters


## Integrations
