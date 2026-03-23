"""백테스트 리포트 생성."""

from backtest.backtester import BacktestResult
from loguru import logger


class ReportGenerator:
    """백테스트 결과를 텍스트/이미지 리포트로 변환."""

    def generate_text(self, result: BacktestResult) -> str:
        """텔레그램 전송용 텍스트 리포트."""
        return f"""📊 백테스트 결과: {result.strategy_name}
기간: {result.start_date} ~ {result.end_date}
총 수익률: {result.total_return:.1%}
샤프비율: {result.sharpe_ratio:.2f}
최대낙폭: {result.max_drawdown:.1%}
승률: {result.win_rate:.1%}
총 거래횟수: {result.total_trades}회
{'✅ 전략 등록 기준 충족' if result.sharpe_ratio > 0.8 else '❌ 전략 등록 기준 미달 (샤프 < 0.8)'}"""

    def generate_chart(self, result: BacktestResult, save_path: str):
        """수익률 곡선 차트 이미지 생성."""
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 6))
        plt.plot(result.equity_curve, label="자산 곡선")
        plt.title(f"{result.strategy_name} 백테스트")
        plt.xlabel("거래일")
        plt.ylabel("자산 (원)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
        logger.info(f"백테스트 차트 저장: {save_path}")
