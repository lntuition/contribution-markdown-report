# Daily contribution chekcer
[![License](https://img.shields.io/github/license/lntuition/daily-contribution-checker)](https://github.com/lntuition/daily-contribution-checker/blob/master/LICENSE)
[![Action](https://github.com/lntuition/daily-contribution-checker/workflows/Daily%20contribution%20checker/badge.svg)](https://github.com/lntuition/daily-contribution-checker/actions?query=workflow%3A%22Daily+contribution+checker%22)

Automatically check daily contribution with `Python` & `Github Actions`.
Every day at 9am, github action will check your contribution and update result.

## How to Use?
1. Fork this project to your account :smile:
2. Modify `.github/workflows/check.yml`
``` yml
env:
  # Change below variable to date you want to start tracking.
  start-date: '2020-07-01'
  auto-update: true
```
3. Enjoy daily contribution checker :tada:

## Feature
### Report
- With new information, daily report is created at **result/README.md**. 
- Report has summary, graph, table section. See example report [here](https://github.com/lntuition/daily-contribution-checker/tree/master/result/README.md)

### Auto update
- Automatic updates can be turned on and off through `auto-update` value in **workflows/check.yml**.
- With enable automatic updates, updated features will be automatically reflected to your repo.
- Forked **workflows/check.yml** does not automatically updated because it has personal settings
- Unfortunately, If there are some changes to workflows, you have to update it manually. But don't worry. I'll notice to every user.

## Notification
- We track your contribution history from your public profile with anonymous user.
  So, if you turn off `Contribution Settings > Private contributions`, private contribution will not be tracked.
- Contribution of the public profile is based on UTC. It should be different from your login profile.

## Bug report & Feature request
- Please leave an [issue](https://github.com/lntuition/daily-contribution-checker/issues). Reporting makes the software more robust :+1:

## License
- [MIT LICENSE](https://github.com/lntuition/daily-contribution-checker/blob/master/LICENSE)
