# Fluid Protocol (BigMath) & Sky (sUSDS) Quant Bot Starter Kit (Python)

An open-source Python monitoring and execution-simulation starter kit for **Fluid Protocol (by Instadapp)** liquidity bots and **Sky (`sUSDS`)** leveraged basis-trade loopers.

> 📡 **Live Proof-of-Concept Feed:** Watch our engine broadcast real-time DeFi quant telemetry every 4 hours on our **[Public Telegram Quant Channel](https://t.me/YOUR_CHANNEL_HANDLE)**.

## The On-Chain Data Bottleneck
If you build automated strategies on **Fluid** or **Sky (`sUSDS`)**, standard ERC-20/ERC-4626 RPC calls fail in production for two reasons:
1. **Fluid's Bit-Packed `BigMathMinified` Storage:** To optimize gas, Fluid's core Liquidity singleton (`0x52Aa...4e497`) does not expose standard human-readable getters. It packs borrow rates, utilization, exchange prices, and totals into single `uint256` words using a custom 64-bit floating-point format (`56-bit coefficient | 8-bit exponent`).
2. **Sky's Un-Dripped `RAY` ($10^{27}$) Rate Accumulator (`chi`):** If `sUSDS.drip()` hasn't been called in the current block, reading `chi()` directly returns stale yield data. Calculating net leveraged ROE against Morpho Blue requires simultaneous `RAY` ($10^{27}$) discrete binary exponentiation (`rpow`) and `WAD` ($10^{18}$) continuous compounding.

---

## Quick Start (Zero Bit-Shifting or RPC Setup Required)

This starter kit uses the **[Stateless DeFi Quant Simulators API on RapidAPI]([YOUR_RAPIDAPI_HUB_URL])** to unpack Fluid's 256-bit storage slots and compute live un-dripped `sUSDS` carry spreads in a single `GET` request.

### 1. Grab a Free API Key
1. Go to the **[DeFi Quant Simulators RapidAPI Hub Page]([YOUR_RAPIDAPI_HUB_URL])**.
2. Subscribe to the **Basic (Free)** tier (`100 requests/month` — no credit card required) or **Pro** for 24/7 bot polling.
3. Copy your `X-RapidAPI-Key` and `X-RapidAPI-Host`.

### 2. Run the Fluid & Sky Carry Bot

    pip install requests
    export RAPIDAPI_KEY="your_key_here"
    export RAPIDAPI_HOST="your_host_here.p.rapidapi.com"
    python fluid_sky_bot.py

---

## Included Popular Fluid Token Addresses (Ethereum Mainnet)

Pass any of these verified ERC-20 addresses into `TOKEN_ADDRESS` inside `fluid_sky_bot.py` (or directly to `/api/v1/fluid/liquidity-state?token=...`):

| Asset | Mainnet ERC-20 Address | Primary Fluid Quant Use Case |
| :--- | :--- | :--- |
| **USDC** *(Default)* | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | Core stablecoin borrow liquidity & utilization tracking |
| **wstETH** | `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0` | Flagship ETH liquid staking collateral & smart-collateral vaults |
| **USDT** | `0xdAC17F958D2ee523a2206206994597C13D831ec7` | Tether borrow rate and supply liquidity monitoring |
| **sUSDe** | `0x9D39A5DE30e57443BfF2A8307A4256c8797A3497` | Ethena staked USDe collateral loops on Fluid |
| **cbBTC** | `0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf` | Coinbase Wrapped BTC liquidity and borrow utilization |
