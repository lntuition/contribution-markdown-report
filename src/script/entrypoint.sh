#!/bin/bash

function GENERATE_REPORT {
    END_DATE=$(date -d "1 day ago" "+%Y-%m-%d")

    python ${SOURCE_PATH}/client/main.py \
        ${GITHUB_ACTOR} ${INPUT_LANGUAGE} ${INPUT_START_DATE} ${END_DATE} ${ARTIFACT_PATH}

    if [ $? -ne 0 ]; then
        echo "Generate report failed, check python trackback"
        exit 1
    fi
}

function CONFIG_REPORT {
    git config http.sslVerify false
    git config --global user.email "${INPUT_AUTHOR_EMAIL}"
    git config --global user.name "${INPUT_AUTHOR_NAME}"
}

function COPY_REPORT {
    REMOTE_URL="https://${GITHUB_ACTOR}:${INPUT_GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"

    git clone --branch "${INPUT_BRANCH}" --single-branch ${REMOTE_URL} ${REPO_PATH}
    cd ${REPO_PATH}
    mkdir -p ${INPUT_PATH}
    cp -rfv ${ARTIFACT_PATH}/* ${INPUT_PATH}
}

function COMMIT_REPORT {
    git add -A
    git commit -m "BOT: ${END_DATE} contribution report"
    if [ $? -ne 0 ]; then
        echo "No changes to commit, pass left process"
        exit 0
    fi
}

function PUSH_REPORT {
    git log -2
    git push origin HEAD:"${INPUT_BRANCH}"
    if [ $? -ne 0 ]; then
        echo "Commit report failed, check bash script"
        exit 1
    fi
}

GENERATE_REPORT
if [ -z "${INPUT_ARTIFACT_ONLY}" ]; then
    CONFIG_REPORT && COPY_REPORT && COMMIT_REPORT && PUSH_REPORT
fi
