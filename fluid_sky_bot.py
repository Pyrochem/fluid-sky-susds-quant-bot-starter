import os
import requests
from datetime import datetime

# =====================================================================
# CONFIGURATION: Get your API key from RapidAPI Hub
# =====================================================================
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY_HERE")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "YOUR_RAPIDAPI_HOST_HERE")

# Default Fluid Token: Mainnet wstETH
FLUID_TOKEN = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
SIMULATED_FLUID_BORROW = 2500  # Simulate borrowing 2,500 wstETH
TARGET_SKY_LEVERAGE = 6        # Simulate a 6x leveraged sUSDS loop

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": RAPIDAPI_HOST
}

def run_fluid_sky_monitor():
    print("\n" + "="*72)
    print(f" 🧩 FLUID BIGMATH & SKY sUSDS CARRY MONITOR | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*72)

    # 1. Query Fluid Protocol BigMath Unpacker Endpoint
    fluid = requests.get(
        f"https://{RAPIDAPI_HOST}/api/v1/fluid/liquidity-state",
        headers=HEADERS,
        params={"token": FLUID_TOKEN, "simBorrowDelta": SIMULATED_FLUID_BORROW},
        timeout=15
    ).json()

    # 2. Query Sky sUSDS (RAY rpow) vs Morpho Carry Simulator
    sky = requests.get(
        f"https://{RAPIDAPI_HOST}/api/v1/sky/susds-carry-simulator",
        headers=HEADERS,
        params={"leverage": TARGET_SKY_LEVERAGE},
        timeout=15
    ).json()

    symbol = fluid["asset"]["symbol"]
    f_supply = fluid["unpackedLiquidityTotals"]["totalSupplyHuman"]
    f_borrow = fluid["unpackedLiquidityTotals"]["totalBorrowHuman"]
    f_avail = fluid["unpackedLiquidityTotals"]["availableLiquidityHuman"]
    f_util = fluid["ratesAndUtilization"]["utilizationPercent"]
    f_borrow_apr = fluid["ratesAndUtilization"]["borrowAprPercent"]
    f_post_util = fluid["stressSimulation"]["postTradeUtilizationPercent"]

    ssr_apy = sky["skySusdsState"]["liveSsrApyPercent"]
    ex_rate = sky["skySusdsState"]["exchangeRateUsdsPerSusds"]
    m_borrow_apy = sky["carrySimulation"]["morphoBorrowApyPercent"]
    net_roe = sky["carrySimulation"]["netLeveragedRoePercent"]
    breakeven = sky["carrySimulation"]["breakevenBorrowApyPercent"]
    regime = sky["carrySimulation"]["carryRegime"]

    print(f"\n💧 1. FLUID PROTOCOL UNPACKED STATE ({symbol})")
    print(f"   • Total Supply / Borrow:   {f_supply:,.2f} {symbol} / {f_borrow:,.2f} {symbol}")
    print(f"   • Available Liquidity:     {f_avail:,.2f} {symbol}")
    print(f"   • Live Utilization & APR:  {f_util:.2f}% util @ {f_borrow_apr:.2f}% Borrow APR")
    print(f"   • Post-Trade Util (+{SIMULATED_FLUID_BORROW}): {f_post_util:.2f}%")

    print(f"\n☀️ 2. SKY (sUSDS) LIVE RAY STATE & {TARGET_SKY_LEVERAGE}x MORPHO CARRY")
    print(f"   • Live Un-Dripped SSR APY: {ssr_apy:.2f}% (1 sUSDS = {ex_rate:.6f} USDS)")
    print(f"   • Benchmark Borrow APY:    {m_borrow_apy:.2f}%")
    print(f"   • Net {TARGET_SKY_LEVERAGE}x Leveraged ROE:    {net_roe:+.2f}% APY")
    print(f"   • Breakeven Borrow Ceiling:{breakeven:.2f}% APY")
    print(f"   • Carry Regime Signal:     [{regime}]")
    print("="*72 + "\n")

if __name__ == "__main__":
    run_fluid_sky_monitor()
