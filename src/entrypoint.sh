#!/bin/bash

VAR_RESULT_DIR="result"
VAR_REMOTE_REPO="https://${GITHUB_ACTOR}:${INPUT_GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
VAR_TARGET_DIR="target"

function FUNC_GENERATE_REPORT
{
    cd ${INPUT_WORKDIR}
    python main.py ${GITHUB_ACTOR} ${INPUT_START_DATE} ${VAR_RESULT_DIR}

    if [ $? -ne 0 ]
    then
        echo "Generate data failed, check python trackback"
        exit 1
    fi
}

function FUNC_PROCESS_REPORT
{
    # Setup git configuration
    git config http.sslVerify false
    git config --global user.email "${INPUT_AUTHOR_EMAIL}"
    git config --global user.name "${INPUT_AUTHOR_NAME}"

    # Move report to target repository
    git clone --branch "${INPUT_BRANCH}" --single-branch "${VAR_REMOTE_REPO}" ${VAR_TARGET_DIR}
    cd ${VAR_TARGET_DIR}
    mkdir -p ${INPUT_PATH}
    cp -rf ${VAR_RESULT_DIR}/* ${INPUT_PATH}

    # Commit & push to target repository
    git add -A
    git commit -m "BOT: $(date -d '1 day ago' '+%Y-%m-%d') contribution check result" || echo "No changes to commit"
    git log -2
    git push "${VAR_REMOTE_REPO}" HEAD:"${INPUT_BRANCH}"

    if [ $? -ne 0 ]
    then
        echo "Commit data failed, check commit bash script"
        exit 1
    fi
}

FUNC_GENERATE_REPORT && FUNC_PROCESS_REPORT
