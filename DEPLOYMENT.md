# Deployment Guide — legacy-to-agentic-ready

The repository is initialized and ready to push to GitHub and/or Gitea.

---

## Push to GitHub

### Using HTTPS (Recommended for most users)

```bash
cd ~/legacy-to-agentic-ready

# Add your GitHub repository as a remote
git remote add origin https://github.com/YOUR_USERNAME/legacy-to-agentic-ready.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Using SSH (For SSH key authentication)

```bash
cd ~/legacy-to-agentic-ready

# Add your GitHub repository as a remote
git remote add origin git@github.com:YOUR_USERNAME/legacy-to-agentic-ready.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Steps:
1. Create a new repository on GitHub (https://github.com/new)
   - Repository name: `legacy-to-agentic-ready`
   - Description: "A toolkit to transform any repository into an AI-agent-ready codebase"
   - Make it Public (recommended)
   - **Do NOT** initialize with README, .gitignore, or license
2. Copy the repository URL from GitHub
3. Run the commands above, replacing `YOUR_USERNAME` with your GitHub username

---

## Push to Gitea

### Using HTTPS

```bash
cd ~/legacy-to-agentic-ready

# Add your Gitea repository as a remote
git remote add gitea https://YOUR_GITEA_INSTANCE/YOUR_USERNAME/legacy-to-agentic-ready.git

# Push to main branch
git push -u gitea main
```

### Using SSH

```bash
cd ~/legacy-to-agentic-ready

# Add your Gitea repository as a remote
git remote add gitea ssh://git@YOUR_GITEA_INSTANCE/YOUR_USERNAME/legacy-to-agentic-ready.git

# Push to main branch
git push -u gitea main
```

### Steps:
1. Log in to your Gitea instance
2. Create a new repository:
   - Repository name: `legacy-to-agentic-ready`
   - Description: "A toolkit to transform any repository into an AI-agent-ready codebase"
   - Make it Public (recommended)
3. Copy the repository URL from Gitea
4. Run the commands above, replacing `YOUR_GITEA_INSTANCE` and `YOUR_USERNAME`

---

## Push to Both GitHub AND Gitea

If you want to mirror this repository to both platforms:

```bash
cd ~/legacy-to-agentic-ready

# Add both remotes
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/legacy-to-agentic-ready.git
git remote add gitea https://YOUR_GITEA_INSTANCE/YOUR_GITEA_USERNAME/legacy-to-agentic-ready.git

# Push to both repositories
git push -u origin main
git push -u gitea main
```

---

## Verify the Push

### Check that remotes are configured:
```bash
git remote -v
# Should show:
# origin  https://github.com/YOUR_USERNAME/legacy-to-agentic-ready.git (fetch)
# origin  https://github.com/YOUR_USERNAME/legacy-to-agentic-ready.git (push)
# gitea   https://YOUR_GITEA_INSTANCE/YOUR_USERNAME/legacy-to-agentic-ready.git (fetch)
# gitea   https://YOUR_GITEA_INSTANCE/YOUR_USERNAME/legacy-to-agentic-ready.git (push)
```

### View repository status:
```bash
# Check log
git log --oneline

# Check current branch
git branch -a

# Check what would be pushed
git status
```

---

## Future Pushes

Once the remotes are configured, future commits and pushes are simple:

```bash
cd ~/legacy-to-agentic-ready

# Make changes
echo "your changes" >> some-file.md

# Commit
git add -A
git commit -m "Your commit message"

# Push to all remotes
git push origin main
git push gitea main
```

---

## Authentication Troubleshooting

### GitHub Authentication Issues

**If using HTTPS:**
- GitHub now requires a Personal Access Token (PAT) instead of passwords
- Create one: https://github.com/settings/tokens/new
- Scopes needed: `repo`, `admin:repo_hook`
- Use the token as your password during `git push`

**If using SSH:**
- Ensure your SSH key is added to GitHub: https://github.com/settings/ssh/new
- Test with: `ssh -T git@github.com`

### Gitea Authentication Issues

**If using HTTPS:**
- Check your Gitea instance supports HTTPS
- Verify your username and password

**If using SSH:**
- Add your SSH public key to your Gitea profile
- Test with: `ssh -T git@YOUR_GITEA_INSTANCE`

---

## Repository URL Formats

### GitHub
- HTTPS: `https://github.com/USERNAME/legacy-to-agentic-ready.git`
- SSH: `git@github.com:USERNAME/legacy-to-agentic-ready.git`

### Gitea (self-hosted)
- HTTPS: `https://gitea.example.com/USERNAME/legacy-to-agentic-ready.git`
- SSH: `ssh://git@gitea.example.com/USERNAME/legacy-to-agentic-ready.git`
- Or: `git@gitea.example.com:USERNAME/legacy-to-agentic-ready.git`

---

## Next Steps

Once the repository is pushed:

1. **Share the repository link** with your team or community
2. **Create documentation** in your GitHub/Gitea README about how to use the toolkit
3. **Test the transformer** on a sample repository to ensure it works as expected
4. **Consider creating releases** for versioning
5. **Set up GitHub Actions** or gitea CI for automated testing (optional)

---

## See Also

- [GitHub Documentation](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-a-repository-with-git)
- [Gitea Documentation](https://docs.gitea.com/)
- [Git Remote Documentation](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)
