#!/bin/bash

# Clone repository
git clone ${INPUT_REMOTE} ${INPUT_LOCAL} && cd ${INPUT_LOCAL}
if [[ ${INPUT_BRANCH} != "" && $(git ls-remote --heads origin ${INPUT_BRANCH}) != "" ]]; then
    git checkout -t remotes/origin/${INPUT_BRANCH}
fi

# Generate report
cd ${INPUT_LOCAL} && mkdir -p ${INPUT_WORKSPACE} && cd ${INPUT_WORKSPACE}
if [[ ${INPUT_END_DATE} == "yesterday" ]]; then
    export INPUT_END_DATE=$(date +%Y-%m-%d -d yesterday)
fi
python /action/main.py

# Push to repository
cd ${INPUT_LOCAL}
git config --global user.name "github-actions[bot]"
git config --global user.email "github-actions[bot]@users.noreply.github.com"
git add ${INPUT_WORKSPACE}
git commit -m "${INPUT_USER}'s contribution report on ${INPUT_END_DATE}"
git log -2

if [[ ${INPUT_PUSH} == "true" ]]; then
    git push origin HEAD:$(git rev-parse --abbrev-ref HEAD)
fi
