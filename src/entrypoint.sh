#!/bin/sh

# Generate data
cd /actions
python src/main.py

# Commit data
git config http.sslVerify false
git config --global user.email "${INPUT_AUTHOR_EMAIL}"
git config --global user.name "${INPUT_AUTHOR_NAME}"

remote_repo="https://${GITHUB_ACTOR}:${INPUT_GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"

git clone --single-branch --branch "${INPUT_BRANCH}" "${remote_repo}" /target
cd /target
mkdir -p ${INPUT_PATH}
cp -rf /actions/result/* ${INPUT_PATH}

git add -A
git commit -m "BOT: $(date -d '1 day ago' '+%Y-%m-%d') contribution check result" || echo "No changes to commit"
git push "${remote_repo}" HEAD:"${INPUT_BRANCH}"
