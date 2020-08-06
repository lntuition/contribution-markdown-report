# Daily contribution chekcer
[![License](https://img.shields.io/github/license/lntuition/daily-contribution-checker)](https://github.com/lntuition/daily-contribution-checker/blob/master/LICENSE)
[![Action](https://github.com/lntuition/daily-contribution-checker/workflows/Daily%20contribution%20checker/badge.svg)](https://github.com/lntuition/daily-contribution-checker/actions?query=workflow%3A%22Daily+contribution+checker%22)

Automatically check daily contribution with `Python` & `Github Actions`.
Whenever you want, github action will check your contribution and update result.

## How to Use?
### With marketplace
1. Add below workflow step in your repository :smile:
``` yml
- name: Daily contribuition checker
  uses: lntuition/daily-contribution-checker@master
  with:
    # Do not change this value unless you know what you are doing now. 
    github_token: ${{ secrets.GITHUB_TOKEN }}
    # Change below variable to date you want to start tracking.
    start_date: "2020-07-01"
    # Branch where the result will be. Default branch is master
    branch: "master"
    # Path where the result will be. Default path is "." which is root directory of repo
    path: "result"
```
2. Enjoy daily contribution checker :tada:

## Feature
### Report
- With new information, daily report is created at **result/README.md**. 
- Report has summary, graph, table section. See example report [here](https://github.com/lntuition/daily-contribution-checker/tree/master/result/README.md)

## Notification
- We track your contribution history from your public profile with anonymous user.
  So, if you turn off `Contribution Settings > Private contributions`, private contribution will not be tracked.
- Contribution of the public profile is based on UTC. It should be different from your login profile.

## Bug report & Feature request
- Please leave an [issue](https://github.com/lntuition/daily-contribution-checker/issues). Reporting makes the software more robust :+1:

## Article
- [Korean : Github Actions 로 Daily Contribution checker 만들기](https://medium.com/@ekffu200098/python-github-actions-%EB%A1%9C-daily-contribution-checker-%EB%A7%8C%EB%93%A4%EA%B8%B0-2fa7f306de46)

## License
- [MIT LICENSE](https://github.com/lntuition/daily-contribution-checker/blob/master/LICENSE)
