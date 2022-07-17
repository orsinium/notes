# Bulk edit settings for GitLab projects

So, you have a bunch of projects on GitLab and you want to edit settings for all of them. For example, disable issues everywhere. There is a little guide how.

We'll actively use the power of bash pipes, so the first thing you need is a good CLI client for GitLab with support for editing settings. I've picked [python-gitlab](https://python-gitlab.readthedocs.io/en/stable/index.html). Let's install it:

```bash
python3 -m pip install -U --user python-gitlab
```

Check if it works:

```bash
gitlab --version
```

Now, let's give it an access. [Generate a personal access token](https://gitlab.com/-/profile/personal_access_tokens) and set it as `GITLAB_PRIVATE_TOKEN` environment variable:

```bash
export GITLAB_PRIVATE_TOKEN="insert-your-token-here"
```

How do you want to filter the projects you want to edit? In my case, I want to edit all projects in a specific group (organization is also considered a group from the API perspective). For that, you need to find out the group ID. So, let's list all groups we have an access to with their name and ID:

```bash
gitlab group list
```

Add `-o json` after `gitlab` if you need more information.

Get IDs for all projects you own (and so can edit) in a specific group:

```bash
gitlab group-project list --group-id YOUR_GROUP_ID --owned=true --all
```

So, how to edit the settings for a given project? There is a subcommand `gitlab project update`. It has a [CLI reference](https://python-gitlab.readthedocs.io/en/stable/cli-objects.html#gitlab-project-update) (you can get the same by executing `gitlab project update -h`) but it doesn't have descriptions for any options. So, you'll also need [the official GitLab API reference](https://docs.gitlab.com/ee/api/projects.html#edit-project), it has a good description for each field. You need both references, though, because the CLI doesn't support some of the API fields.

So, if you want to disable issues for a project with ID 123:

```bash
gitlab project update --issues-access-level disabled --id 123
```

The output is pretty verbose. When we runn it in a loop, it will bloat the terminal. The tool has `--fields` option but somehow it doesn't work for me. So, instead we'll output the result as a JSON and filter it using [jq](https://stedolan.github.io/jq/) (install it with `sudo apt install jq`):

```bash
gitlab -o json project update --issues-access-level disabled --id 123 | jq .name
```

And now, let's glue everything together. We'll use [grep](https://en.wikipedia.org/wiki/Grep) to extract IDs from the `gitlab group-project list` output and [xargs](https://en.wikipedia.org/wiki/Xargs) to call `gitlab project update` with each ID as the last argument. Here is the result:

```bash
gitlab group-project list --group-id {{.GROUP_ID}} --owned=true --all \
    | grep -oE '[0-9]+' \
    | xargs -n1 gitlab -o json project update --issues-access-level disabled --id \
    | jq .name
```

I hope it saved your day.

## Bonus: Taskfile

I use [task](https://taskfile.dev) for automating things. It's like [make](https://en.wikipedia.org/wiki/Make_software) but for normal humans. There is my taskfile for diabling everything that can be disabled on GitLab for a specific group:

```yaml
# https://taskfile.dev
version: '3'

vars:
  GROUP_ID: "123456"

env:
  GITLAB_PRIVATE_TOKEN:
    sh: cat .token

tasks:
  install:
    status:
      - which gitlab
    cmds:
      - python3 -m pip install -U --user python-gitlab
  groups:
    cmds:
      - gitlab -o json group list
  bulk-update:
    deps:
      - install
    cmds:
      - >
        gitlab group-project list --group-id {{.GROUP_ID}} --owned=true --all
        | grep -oE '[0-9]+'
        | xargs -n1
        gitlab -o json project update
        --analytics-access-level              disabled
        --auto-devops-enabled                 false
        --container-registry-enabled          false
        --forking-access-level                disabled
        --issues-access-level                 disabled
        --operations-access-level             disabled
        --pages-access-level                  disabled
        --packages-enabled                    false
        --remove-source-branch-after-merge    true
        --service-desk-enabled                false
        --snippets-access-level               disabled
        --squash-option                       default_off
        --wiki-access-level                   disabled
        {{.CLI_ARGS}} --id
        | jq .name

  run:
    deps:
      - install
    cmds:
      - gitlab {{.CLI_ARGS}}
```
