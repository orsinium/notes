# Blog posts about rewriting a project on Rust are biased

## "Latest versions" bias

Programming languages and frameworks evolve over time. They get better performance and more cool features, and the first thing you should do before considering just ditching everything for a better language is to upgrade all the tools you have.

For example, [Discord switched from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust) primarily because of the CPU usage spikes caused by Go's garbage collector. Many people criticized them for using Go 1.9 (they later updated the post to say they tried 1.10 too) while 1.12 was available. Each new version improves the garbage collector (and perfomance overall) a lot, and upgrading is very easy.

Many blog posts fall for this bias. Even if they upgrade everything before the migration, the benchmarks you see in posts compare what they had a long time ago, before the rewrite, to what they have now. When starting a new project version from scratch, people naturally pick the latest versions for all tools and libraries, and that's where a part of the performance (and developer experience) improvement comes from.

So, before you make the decision to rewrite everything, upgrade every tool you use. And even then, maybe also wait a bit for hardware and tools to get better.

## "Modern technologies" bias

Often, the target for the rewrite is an old legacy project that was written on what at the time had been a brand new thing but isn't that nice looking in the modern world. For example, if you have a [Django](https://www.djangoproject.com/) monolith written 5 years ago or so, you miss on the features of the modern Python, like type annotations (with quite reliable [mypy](https://github.com/python/mypy) type checker) and async/await that makes a project with lots of IO-bound operations (which is any web app that works with a database a third-party APIs) much faster. If you take that project, move to [FastAPI](https://github.com/tiangolo/fastapi), fully type annotate, and use async/await-based frameworks for all IO-bound operations, you'll get miles ahead of what you had in terms of performance and maintainability.

## "Refactoring" bias

When you rewrite a project to another language, you go through every line of code in it and improve it along the way. You find and drop dead code, optimize some places, get rid of some bad decisions, remove unnecessary abstractions. This is one of the reasons why the new code looks cleaner, works better, and runs faster. And that's something you can and should do for your project regardless of if you rewrite it to a new language or not. The [boy scout rule](https://deviq.com/principles/boy-scout-rule) should be part of the engineering culture in your company.

## "Deprecated features" bias

Most of the programming languages evolve over time, and old languages evolved a lot. For instance, ...

## "Bottleneck performance" bias

...

## "Language of choice" bias

...

## "Senior engineers" bias

...

## "Correctness is reliability" bias

...

## "Survivorship" bias

...

## Examples

...

## Sometimes, you should migrate

The goal of this blog post is to warn you about certain biases when considering rewriting everything on Rust (or another language) rather than discourage you from doing so. There are often valid reasons to rewrite everything.

1. There is no universal language that fits all tasks. Each programming language makes certain trade-offs and design choice to fit a certain target audience and a certain set of task. Some languages have manual or semi--manual memory management, some have a garbage collector. Some encourage loops, some prefer recursion. Some are built on top of immutable collections, some prefer mutating things in place for better performance. Rust values the most high CPU perofrmance, small memory footprint, and correctness. So, it fits system programming tasks (writing drivers and games, programming microcontrollers and satelites) much better than Python or JS.
1. Languages, like any other tools, get outdated. They accumulate legacy, slow in development, shrink in size of community and ecosystem. Imagine wtill having a project on Fortran in 2023. It's hard to find engineers to work on it, hard to find new libraries for modern tasks, hard to get community support.
