---
title: "(draft) Collectibles for considering block chain security."
date: 2022-05-29
classes: wide
---

DeFi will be successor of finance, and I guess at least they will take over "Systems" in finance, as AWS has taken over Data centres in TradFi.
Every good aspects there, but security is the major concerns on this domain, so I would like to start accumulaton of incidents, movements of security related.

This page is just for reference. Things are accumulated by each attack vector. I will post another entry everytime my consideration will have been popped out of my head.

## Wallet (EOA)

- Issue
  - You are unaware when/whether your key compromized.Key diversification is plus for lost-proof.
    - it is prone to exploit(for SW) and
    - prone to steal  (for HW)
- Design
  - Gnosis safe

## Smart Contract

- Reentry attack
  - Incidents
    - Rari fuse <https://twitter.com/feiprotocol/status/1520344430242254849>
- Expoint of governance Vote on DAO
  - Incidents
    - Deus DAO <https://cryptoslate.com/deus-dao-suffers-another-flash-loan-exploit-loses-over-16m/>
  - Counter act
    - Check timestamp <xxx>
    - Check result of proposal, in simulated environment
      - Uniswap <https://uniswap.org/blog/governance-seatbelt>
      - Aave Seatbelt <https://governance.aave.com/t/bgd-release-aave-seatbelt/8310>

## Liquidity

- Triggerring doom loop
  - UST <https://twitter.com/OnChainWizard/status/1524123935570382851>
    - although actually UST has fallen as acted by design
  - Nansen's impressive on chain analysis <https://www.nansen.ai/research/on-chain-forensics-demystifying-terrausd-de-peg>

