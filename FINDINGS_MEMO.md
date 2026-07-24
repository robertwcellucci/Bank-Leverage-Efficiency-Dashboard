# Memorandum

**To:** Credit Risk Committee
**From:** Robert Cellucci
**Date:** July 2026
**Re:** Leverage and profitability screen, 260 U.S. bank holding companies (FY2025 10-K filings)

---

## Summary

Small banks in this sample carry meaningfully more leverage than large banks while earning
less on their assets. Average leverage runs 10.64x in the smallest asset quartile against
9.14x in the largest.

The practical consequence: **64 of 242 banks (26%) sit in the quadrant that warrants
review**, above 10x leverage and below the 1.04% median ROA. Small banks are flagged at
roughly double the rate of the other two tiers: 46% of the small-bank population falls
into the flagged group, versus 19% of mid-tier and 21% of large-tier banks.

Leverage and ROA are negatively correlated across the sample (r = -0.30). Leverage is not
buying returns here. That is the finding worth acting on.

---

## What the screen shows

| Size tier | Banks | Avg leverage | Median ROA |
|---|---|---|---|
| Small | 61 | 10.64x | 0.90% |
| Mid | 119 | 9.25x | 1.11% |
| Large | 62 | 9.14x | 1.07% |

Leverage falls monotonically with size; ROA does not rise monotonically to match. The
small-bank tier is the outlier on both measures simultaneously, which is the combination
that matters for credit review.

**Highest-leverage names in the flagged quadrant:**

| Bank | Leverage | ROA | Assets |
|---|---|---|---|
| Union Bankshares Inc | 20.0x | 0.69% | $1.6B |
| Uwharrie Capital Corp | 18.4x | n/a | $1.2B |
| Juniata Valley Financial Corp | 15.6x | 0.89% | $0.9B |
| West Bancorporation Inc | 15.6x | 0.79% | $4.1B |
| BayFirst Financial Corp | 14.8x | -1.76% | $1.3B |
| HSBC USA Inc | 13.9x | 0.64% | $172.4B |
| Northern Trust Corp | 13.7x | 0.98% | $177.1B |
| State Street Corp | 13.1x | 0.80% | $366.0B |

Uwharrie Capital Corp appears here on leverage alone; its ROA is genuinely unreported
(see Limitations, below) rather than a computed value below the threshold, so it is
listed for visibility but not counted in the 64-bank flagged total.

Ten banks in the sample reported negative net income; five of those also exceed 10x
leverage. That group is the narrowest and most defensible starting point for review.

---

## Charter type is not a useful discriminator

State-chartered (SIC 6022) and nationally chartered (SIC 6021) banks are effectively
indistinguishable on both measures: 9.58x leverage and 0.97% ROA for state banks against
9.55x and 1.00% for national. Charter type does not carry information for this screen and
should not be used as a segmentation variable. Size tier should.

---

## Concentration note

The five largest institutions hold 63% of total assets in the sample ($21.2T aggregate).
Any asset-weighted average is therefore a statement about JPMorgan, Bank of America,
Citigroup, Wells Fargo, and US Bancorp rather than about the banking population. All
figures in this memo are unweighted per-bank averages for that reason. If the committee
wants a system-exposure view rather than an institution-screening view, the weighting
should be changed deliberately and the difference noted.

---

## Limitations

1. **Missing XBRL tags were being misread as zero; this has been corrected.** The
   workbook originally pulled financial values through `GETPIVOTDATA`, which returns a
   literal 0 for a blank pivot cell rather than an error when a filer has no row for a
   given tag. Nine banks, including Truist and PNC, had no `NetIncomeLoss` value that
   survived the fiscal-period filter, and the workbook was rendering that gap as 0%
   ROA rather than a true unknown. Left uncorrected, that pulled average ROA down by
   roughly 4 basis points. The lookups for Assets, Liabilities, Interest, NetIncomeLoss,
   and StockholdersEquity now check tag existence directly against the source filings
   (`COUNTIFS` against the raw `financials` sheet) before trusting the pivot value; a
   genuinely missing tag now returns blank and is excluded from every average, rather
   than silently entering as zero. The figures in this memo reflect that corrected
   treatment throughout.

2. **Twelve banks excluded entirely** (260 filings, 248 with computable ratios, 242 after
   removing the zero-earnings artifacts above). Most are missing `StockholdersEquity`,
   which makes leverage undefined. First United Corp and First Internet Bancorp are
   missing all core tags.

3. **Point-in-time balance sheet.** Leverage is computed from period-end assets and equity
   in a single filing. No trend, no quarterly volatility, no off-balance-sheet exposure.
   A bank that delevered sharply during the year looks identical to one that did not.

4. **Accounting leverage, not regulatory capital.** Assets/Equity is not Tier 1, is not
   risk-weighted, and says nothing about asset quality. A bank at 12x holding Treasuries
   is not comparable to a bank at 12x holding CRE. This screen orders names for review;
   it does not assess adequacy.

5. **Correlation only.** The size-leverage relationship is descriptive. Nothing here
   establishes that small size causes higher leverage, and plausible confounders (funding
   mix, regional CRE concentration, M&A history) are unmeasured.

---

## Recommended next steps

1. Pull risk-weighted capital ratios for the 64 flagged banks; re-rank on Tier 1 rather
   than accounting leverage.
2. Screen the five negative-earnings, high-leverage banks first.
3. Reclassify custody banks out of the general peer group.
4. Add three years of filings to convert this from a snapshot into a trend screen.

---

*Source: SEC EDGAR Financial Statement Data Sets (sub.txt, num.txt), FY2025 10-K filings,
SIC 6021 and 6022. Full methodology and workbook in this repository.*
