# polyglot-info

Static site for polyglot-info.org published with Cloudflare Pages.

This repo includes a GitHub Actions workflow that generates a new article on a schedule and rebuilds the homepage with links to all articles.

## How it works
- scripts/build.py creates a new article (HTML) in /articles/ and regenerates index.html to list all articles.
- The workflow .github/workflows/auto-update.yml runs every 12 hours (and can be triggered manually), commits new content, and pushes to main. Each push triggers Cloudflare Pages to deploy.

## One-time setup
1) Create the repo on GitHub and upload these files.
2) In Cloudflare Pages, create a Project and connect it to this GitHub repo.
   - Framework: None
   - Build command: (leave empty)
   - Output directory: /  (root)
3) Set your custom domain: polyglot-info.org.

## Change the cadence
Edit the cron in .github/workflows/auto-update.yml:
- cron: "0 */12 * * *"
