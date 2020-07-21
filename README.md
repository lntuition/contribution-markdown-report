# Daily contribution chekcer
![License](https://img.shields.io/github/license/lntuition/daily-contribution-checker)
![Action](https://github.com/lntuition/daily-contribution-checker/workflows/Daily%20contribution%20checker/badge.svg)  
Automatically check daily contribution with `Python` & `Github Actions`.
Every day at 9am, github action will check your contribution and update result.

## How to Use?
1. Fork this project to your account :smile:
2. Modify `.github/workflows/check.yml` and remove `result/data.csv`
``` yml
env:
  # Change below variable to date you want to start tracking.
  # This date(YYYY-MM-DD) must be within a year.
  start-date: '2020-07-01'
```
3. Enjoy daily contribution checker :tada:

## Notification
- We track your contribution history from your public profile with anonymous user.
  So, if you turn off `Contribution Settings > Private contributions`, private contribution will not be tracked.
- Contribution of the public profile is based on UTC. It should be different from your login profile.
- Data initialization is performed only the first time.
  If you want to reset data, you need to delete `result/data.csv` manually.

## Bug report & Feature request
- Please leave an [issue](https://github.com/lntuition/daily-contribution-checker/issues). Reporting makes the software more robust :+1:

## License
- [MIT LICENSE](https://github.com/lntuition/daily-contribution-checker/blob/master/LICENSE)
