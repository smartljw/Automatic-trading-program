# /deploy

프로덕션 배포를 실행합니다.

## 사용법
```
/deploy [환경: staging|production]
```

## 실행 단계
1. 테스트 전체 실행 (`pytest tests/`)
2. Docker 이미지 빌드
3. 현재 봇 안전하게 정지 (포지션 유지)
4. 새 버전 배포
5. 헬스체크 확인
6. 텔레그램으로 배포 완료 알림

## 주의사항
- production 배포 전 반드시 사용자 확인 요청
- `KIS_PAPER_TRADE=true` 확인 후 배포
