# Contribution markdown report
[![License](https://img.shields.io/github/license/lntuition/contribution-markdown-report)](https://github.com/lntuition/contribution-markdown-report/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/lntuition/contribution-markdown-report/branch/master/graph/badge.svg?token=TDAMA0FK7C)](https://codecov.io/gh/lntuition/contribution-markdown-report)

Automatically generate contribution markdown report with `Python` & `Github Actions`.
Whenever you want, github action will check your contribution and update result.

## Usage
- Add below workflow step to your repository
``` yml
jobs:
  example:
    runs-on: ubuntu-latest

    steps:
    - uses: lntuition/contribution-markdown-report@master
      with:
        # Branch where the report will be updated, default is default branch
        branch: ""
        # Relative path where the report will be updated, default is ${repository}/result
        workspace: "result"
        # Name of markdown report file, default is README
        file_name: "README"

        # User of report, default is repository owner
        user: "lntuition"
        # Start date in report, following isoformat
        start_date: "2020-07-01"
        # End date in report, default is yesterday.
        # Except for yesterday keyword, following isoformat
        end: "yesterday"
        # Language used in report, default is english
        langugage: "english"
```

## Notification
- We track your contribution history from your public profile with anonymous user.
  So, if you turn off `Contribution Settings > Private contributions`, private contribution will not be tracked.
- See example report [here](https://github.com/lntuition/contribution-markdown-report/blob/master/result/README.md). Example will be updated on every saturday.

## Bug report & Feature request
- Please leave an [issue](https://github.com/lntuition/contribution-markdown-report/issues).
- We are also welcome to contribute directly, see [contribue guide document](https://github.com/lntuition/contribution-markdown-report/blob/master/docs/CONTRIBUTING.md).

## License
- [MIT LICENSE](https://github.com/lntuition/contribution-markdown-report/blob/master/LICENSE)
