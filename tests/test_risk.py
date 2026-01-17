from apps.worker.risk import RiskConfig, check_circuit_breaker


def test_circuit_breaker_daily_loss():
    config = RiskConfig(
        base_risk=0.0025,
        c_min=0.55,
        max_positions=10,
        max_gross_exposure=1.5,
        sector_concentration=0.25,
        daily_max_loss=0.03,
        drawdown_max=0.1,
    )
    state = check_circuit_breaker(daily_loss=-0.04, drawdown=0.02, config=config)
    assert state.tripped is True
    assert state.reason == "daily loss limit exceeded"
