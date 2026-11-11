"""Builds the GitLab version of the profile README.

Same text as README.md, with each GitHub address replaced by its GitLab twin.
Usage: python3 gitlab_readme.py README.md OUTPUT.md
"""
import re
import sys

# GitHub -> GitLab, most specific first so a bare repository link
# never swallows its /tags or badge variants.
REPLACEMENTS = [
    ("https://img.shields.io/github/v/tag/jzbakh/antigravity-arn-skin", "https://img.shields.io/gitlab/v/tag/arn_inside/arn-skin"),
    ("https://img.shields.io/github/stars/jzbakh/antigravity-arn-skin", "https://img.shields.io/gitlab/stars/arn_inside/arn-skin"),
    ("https://github.com/jzbakh/antigravity-arn-skin/tags", "https://gitlab.com/arn_inside/arn-skin/-/releases"),
    ("https://github.com/jzbakh/antigravity-arn-skin", "https://gitlab.com/arn_inside/arn-skin"),
    ("https://img.shields.io/github/v/tag/jzbakh/antigravity-arn-lifebar", "https://img.shields.io/gitlab/v/tag/arn_inside/antigravity-arn-lifebar"),
    ("https://img.shields.io/github/stars/jzbakh/antigravity-arn-lifebar", "https://img.shields.io/gitlab/stars/arn_inside/antigravity-arn-lifebar"),
    ("https://github.com/jzbakh/antigravity-arn-lifebar/tags", "https://gitlab.com/arn_inside/antigravity-arn-lifebar/-/releases"),
    ("https://github.com/jzbakh/antigravity-arn-lifebar", "https://gitlab.com/arn_inside/antigravity-arn-lifebar"),
    ("https://github.com/jzbakh/portfolio-data-analyst", "https://gitlab.com/jzbakh/portfolio-data-analyst"),
    # Badge descriptions that name the forge
    ("GitHub Release Version", "GitLab Release Version"),
    ("GitHub repository stars", "GitLab repository stars"),
    ("GitHub Actions CI/CD", "GitLab CI/CD"),
]

source, target = sys.argv[1], sys.argv[2]
with open(source, encoding="utf-8", newline="") as f:
    text = f.read()

for github, gitlab in REPLACEMENTS:
    text = text.replace(github, gitlab)

# A GitHub address left over means a new project without its GitLab twin:
# fail loudly instead of publishing a GitLab profile that links to GitHub.
leftovers = sorted(set(re.findall(r"https://(?:github\.com|img\.shields\.io/github)/[^\s)\"'>]+", text)))
if leftovers:
    sys.exit("No GitLab address for:\n  " + "\n  ".join(leftovers)
             + "\nAdd it to REPLACEMENTS in .github/gitlab_readme.py")

with open(target, "w", encoding="utf-8", newline="") as f:
    f.write(text)
