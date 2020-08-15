# 일일 컨트리뷰션 검사기
`Python` & `Github Actions` 을 통해 자동적으로 일일 컨트리뷰션 정보를 추적합니다. 
원할때 언제든, 깃허브 액션이 당신의 컨트리뷰션을 체크하고 결과를 업데이트할 수 있습니다.

## 사용방법
### 마켓플레이스
1. 레포지토리 안에 아래와 같은 워크플로우를 추가합니다 :smile:
``` yml
- name: Daily contribuition checker
  uses: lntuition/daily-contribution-checker@master
  with:
    # 특정한 이유가 있지 않다면 아래의 값을 바꾸지 않는것을 권장합니다.
    github_token: ${{ secrets.GITHUB_TOKEN }}
    # 리포트에서 체크를 시작할 날짜입니다.
    start_date: "2020-07-01"
    # 결과가 생성될 브랜치명입니다. 기본 값은 master 입니다.
    branch: "master"
    # 결과가 생성될 경로입니다. 기본 경로는 ".", 해당 브랜치의 최상위 폴더입니다.
    path: "result"
```
2. 일일 컨트리뷰션 검사기를 즐겨주세요 :tada:

## 특징
### 리포트
- 매일 새로운 정보를 통해 일일 리포트가 설정한 경로에 만들어집니다. 
- 리포트는 요약, 그래프, 표 부분으로 이루어져있습니다. 예시 리포트를 [여기](https://github.com/lntuition/daily-contribution-checker/tree/master/result/README.md)에서 확인해보세요
- 추후 한국어 버전 리포트를 추가할 생각입니다.

## 정보
- 비로그인 상태로 해당 사용자의 컨트리뷰션 정보를 추적합니다. 만약 `Contribution Settings > Private contributions` 옵션을 끈 상태라면, 공개되지 않은 컨트리뷰션 정보는 체크되지 않을것입니다.
- 공개 프로필의 컨트리뷰션 정보는 UTC 시간을 기반으로 합니다. 해당 정보는 로그인 프로필과는 조금 다를 수도 있습니다.
- 마켓플레이스에서 액션을 사용중이라면, Star나 Watch를 남겨주세요. 중요한 변화가 있을때 사용자에게 직접 정보를 전달해드리겠습니다.

## 버그 리포트 & 요청 사항
- [이슈](https://github.com/lntuition/daily-contribution-checker/issues)를 남겨주세요. 리포트는 더 좋은 소프트웨어를 만드는 데 큰 도움이 됩니다. :+1:

## 게시물
- [Github Actions 로 Daily Contribution checker 만들기](https://medium.com/@ekffu200098/python-github-actions-%EB%A1%9C-daily-contribution-checker-%EB%A7%8C%EB%93%A4%EA%B8%B0-2fa7f306de46)

## 라이센스
- [MIT LICENSE](https://github.com/lntuition/daily-contribution-checker/blob/master/LICENSE)
