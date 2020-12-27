# Contributing guide
If you're reading this, you're probably looking to contribute to `contribution-markdown-report`.
First of all thank you very much, please read the guide below.

# Setting up development environment
1. Install `docker` and `make`
1. Use `make build` to make docker image
  - If there are some problem to setup environment, try below guides
    - Use `make build-clean` and re-build docker image
    - Reinstall `docker` and `make`
    - If it still fails, please leave an [issue](https://github.com/lntuition/contribution-markdown-report/issues)
1. Implement feature or modifications and tests
1. Use `make isort` and `make black` to check lint
1. Use `make unit` and `make integration` to test code
  - After doing integration, result with be generated to output folder
  - Use `make clean` to remove output easily

## Pull request
- Make sure your code follows linter
  - Use `make isort-fix` and `make black-fix`
- Make sure your new code to be tested
  - Use `make unit` and `make integration`
  - If it is hard to test, please describe the reason in PR message
- Make sure your commit message follow below rules
  - Subject line must follow template, `{keyword}: {description}`
  - Use the body to explain what and why vs. how 

### Architecture
- Class Diagram
![architecture-name](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/lntuition/contribution-markdown-report/master/docs/architecture.iuml)
