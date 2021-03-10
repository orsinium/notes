# Release every hour

How long is your sprint? How often do you release the product? 2 weeks? 1 week? Every day? Can you do it continiously? Like, every hour. Sounds like a good challenge. Let's take this insane goal and look at our daily processes from the new perspective.

**DISCLAMER:** It is not a success story and isn't a ready-to-use methodology developed by an old and smart scrum master from a huge famous corporation. I'm not a Kent Beck nor Bob Martin, I'm a simple software engineer who is brave enough to ask stupid questions and find equally stupid and obvious solutions.

## Assumptions

Let me first make some assumptions about your company. Most likely, most of them are wrong because I assume the worst scenario. Let's talk about [The Phoenix Project](https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business/dp/0988262592):

+ **The project is old**. It has a lot of code that is referenced only as "legacy", people who made 90% of this are left the company many years ago, the company is considered explusively a corporation, the "startup culture" phrase is only a buzzword.
+ **Tests are awful**. They are slow, every small change breaks all the tests, to run them you need the whole production infrastructure. Probably, you even don't have CI and even if you do, there are only 2-3 jobs and each of them is slow as hell.
+ **The team is big**.
+ **There are many teams**.
+ **The team is unexperienced**.
+ **The team is emotional**.
+ **People are leaving and coming every week**.
+ **Everything seems to be broken**.
+ **There are regulations**.
+ **There are external deadlines**.
+ **Everything is always on fire**.
+ **You always don't have enough people**.
+ **There was no major features for many years**.

## Issues

First of all, let's identify the enemy. The processes that slow us down. Everything, every small details that stands between us and the real continious delivery. Let's be honest and write down every stupid reason, even if we used to it.

+ **Daily standup**. Daily standup isn't bad on its own. If it is done properly, it's a good enough way to keep the team synced on what's going on in 2-week releases. However, our goal is to have much shorter release cycle, so daily standup doesn't work anymore. Also, since the standup takes noticeable time and disrupts the team workflow, we can make it hourly. So, from now on, it is an obstacle we need to avoid to reach the goal.
+ **Bugs**. Every bug is our enemy. Fixing and reporting them takes time, having too much of them makes the product unstable and disappoints users. We don't want to spend time, so we don't want to have too many bugs.
+ **Bad code reviews**. Humans make mistakes. And also they are lazy. Ask someone to review 10k lines of changes, and the person, most probably, will just scroll through it and approve. And even for small changes, the reviewer can miss even quite obvious bugs. While we rely on humans, the code review will be bad.
+ **Slow code reviews**.
+ **Lazy developers**.
+ **Slow communications**.
+ **Slow maintenance**.
+ **Bad estimations**.
+ **Writing documentation**.
+ **Boring tasks**.
+ **Slow tests**.
+ **Onboarding**.
+ **Offboarding**.

## Better management

## Better development
