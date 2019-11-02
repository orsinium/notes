# Multiple accounts for Github

Github doesn't allow you to use the same SSH key for multiple accounts, because in this case server wouldn't detect by your key which account you want to use. Fortunately, Github makes correct redirects from subdomains. Let's use it.

Add new ssh key:

```bash
ssh-keygen -t rsa -C "newuser@yourteam.com" -f .ssh/id_rsa_newuser
ssh-add ~/.ssh/id_rsa_newuser
```

Create `~/.ssh/config` with following rule to say ssh use new key for new domain:

```
Host github.com-newuser
  	HostName yourteam.github.com
  	User git
  	IdentityFile ~/.ssh/id_rsa_ewuser
```

Add this line in your `/etc/hosts`:

```
192.30.253.113  yourteam.github.com
```

That's all! Now use `yourteam.github.com` instead of `github.com` in your remote URL.
