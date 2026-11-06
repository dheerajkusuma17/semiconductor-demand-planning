# Industry Primer: How Semiconductor Demand Planning Works

Read this before Day 1. Five real stories, each with the **lesson for a demand planner** and **where it shows up in this project**. After them come the key concepts and a comparison with biotech / pharma.

Every figure is fact-checked and sourced (links at the bottom), and phrased so you can quote it safely in an interview.

---

## Story 1: The 2021 auto chip shortage
*Long lead times punish bad forecasts.*

When COVID hit in 2020, automakers **cut chip orders**, expecting car sales to collapse. Chip foundries gave that capacity to booming PC and electronics demand. Car sales recovered faster than expected, and automakers couldn't get back in line [1][2]. Just-in-time inventory, reliance on older "legacy" chips and later panic over-ordering made it worse.

Why couldn't it be fixed quickly?
- Making a finished wafer takes **about 12 weeks** on average (14–20 weeks for advanced processes).
- Assembly, test and packaging add **about 6 more weeks**, so order-to-delivery can reach about **26 weeks** [3].
- Average chip lead times passed **20 weeks in mid-2021**, against about 13 weeks normally (Susquehanna data). Some microcontrollers were quoted at **a year or more** [4][5].

The cost:
- AlixPartners estimated in 2021 that the shortage would cost automakers about **$210 billion in revenue and 7.7 million vehicles** of production that year [6].
- Ford and GM built vehicles without some chips and **parked tens of thousands of them**, many F-150s and other pickups, until parts arrived [7][8].

> **Planner lesson:** in semiconductors you commit to supply **about 6 months before you sell**. Today's forecast error becomes next half-year's shortage or glut, and you can't "expedite" a fab.
>
> **In this project:** lead time drives the safety-stock formula (SS = z · σ · √LT). Day 5 includes a sensitivity analysis on how safety stock grows as lead time grows.

---

## Story 2: The bullwhip, 2021 → 2023
*Orders are not demand.*

During the shortage, customers **double-ordered** from several suppliers to secure allocation, and orders looked like record demand [9]. When PC and phone demand fell in 2022, customers cut orders and lived off the inventory they'd built:
- Memory prices collapsed. In Q4 2022, contract prices fell about 23% for DRAM and 28% for NAND.
- **Samsung's Q1 2023 operating profit fell about 95%**, and its chip division lost money.
- **SK hynix** posted a record quarterly loss [10].
- **Micron** posted a record $2.3B quarterly loss, including about **$1.4B of inventory write-downs** [11].

This is the **bullwhip effect**: small changes in end demand become huge swings in upstream orders.

> **Planner lesson:** a semiconductor planner always asks *"Is this real end-market demand, or customers building inventory?"* They watch **book-to-bill**, **channel inventory** (weeks of supply sitting at distributors), and **sell-in vs. sell-through** (POA vs. POS).
>
> **In this project:** the Intel data records **customer orders**, not end consumption. Day 1 looks for order spikes and drops that may be ordering behaviour rather than true demand.

---

## Story 3: Intel and the biased forecast
*Measure bias, not just accuracy.*

In Intel's embedded-products group, the demand forecast was owned by **Sales & Marketing** and loaded directly into the planning (MRP) system. It was **systematically biased**, and the planners who set inventory couldn't change it. Manary & Willems, the same authors who published our dataset, developed a way to **adjust the safety-stock targets for the bias**, using the history of forecast errors, rather than fixing the forecast [12].

> **Planner lesson:** bias is a separate problem from accuracy.
> - A forecast can look "about right" on average across products and still be consistently high for some and consistently low for others.
> - Safety stock should be built from the **forecast error distribution**, corrected for bias, not from raw demand variability.
> - Forecasts are often biased for organisational reasons. Sales teams may forecast high to make sure supply is available.
>
> **In this project:** Day 2 measures Intel's forecast bias, its size **and** its statistical significance. Day 5 builds safety stock from bias-corrected forecast errors.

---

## Story 4: Product generations and end of life
*Every product has a life cycle.*

New CPU and GPU generations typically arrive **every 1–2 years**. Nvidia moved its data-center GPUs to a **yearly** cadence in 2024 [13]. When a new generation launches:
- the new part ramps up;
- the older part loses pricing power (ASP erosion) and demand decays;
- eventually the older part is **discontinued**. Intel issues formal discontinuance notices with a **last order date** (the "last-time buy") and a last ship date [14].

> **Planner lesson:** under-forecasting a ramp loses market share; over-forecasting a tail creates **obsolete inventory** that gets written off. Semiconductor forecasting must be **life-cycle aware**. A model that simply extends the recent trend will overshoot a dying product.
>
> **In this project:** the Intel data covers **several product generations**. Day 1 plots their life-cycle curves, and the ML models (Day 4) use "generation" and "weeks since launch" features.

---

## Story 5: The AI boom, 2023 → today
*Constrained supply and allocation.*

From 2023, supply of Nvidia's AI GPUs was limited by two bottlenecks:
- TSMC's **CoWoS advanced packaging**. In 2023 TSMC said it could meet only about 80% of demand [15].
- **High-bandwidth memory (HBM)**. SK hynix and Micron said HBM was **sold out for 2024 and largely booked for 2025** [16].

Suppliers had to **allocate** limited output across customers.

> **Planner lesson:** separate the **unconstrained demand forecast** (what customers want) from the **constrained supply plan** (what we can ship). The gap is decided in **S&OP / IBP** meetings through allocation rules. A planner who only reports one number is missing half the job.
>
> **In this project:** the Streamlit app and Power BI dashboard present results the way an S&OP deck would: demand, forecast quality, and inventory risk.

---

## What a semiconductor demand planner needs to know

**Supply chain shape**
```
Wafer fab (~12 wks) → Die bank (strategic buffer) → Assembly & test (~6 wks) → Finished goods → OEMs / Distributors (Arrow, Avnet…)
```
The **die bank** stores finished wafers before final packaging. It's the push-pull boundary: produce to forecast before it, finish to order after it.

**Key terms**

| Term | Meaning |
|---|---|
| Bookings / billings / backlog | Orders received / orders shipped and invoiced / orders not yet shipped |
| **Book-to-bill ratio** | Bookings ÷ billings. Above 1 means demand is growing faster than shipments |
| **NCNR** | Non-cancellable, non-returnable orders, used in shortages to stop phantom orders |
| **LTA** | Long-term agreement: a customer commits volume, the supplier commits supply |
| **Allocation** | Rationing scarce supply across customers |
| **ASP erosion** | The average selling price declines over a product's life |
| **EOL / last-time buy** | End of life: the customer's final chance to order a discontinued part |
| **Channel inventory** | Stock sitting at distributors, measured in weeks of supply |
| **POA vs. POS** | Point of authorisation (sell-in to the distributor) vs. point of sale (sell-through to the end customer) |
| **E&O** | Excess & obsolete inventory: the write-off risk |

**Market indicators planners watch**
- WSTS / SIA monthly global chip sales
- SEMI equipment billings
- U.S. Census M3 orders and shipments (used in this project via FRED)
- End-market trends: PCs, smartphones, autos, data centers / AI

**Planner KPIs**
- Forecast accuracy and **bias at the lag that matters** (e.g. the forecast made 3 months before)
- Days of inventory (DOI)
- On-time delivery
- Quoted lead time
- E&O value

**Tools beyond Excel**
- Statistical, ML and neural forecasting (this project)
- S&OP / IBP platforms (SAP IBP, o9, Kinaxis, Blue Yonder)
- BI dashboards (Power BI)

---

## Semiconductor vs. biotech / pharma demand planning

| Dimension | Semiconductor | Biotech / Pharma |
|---|---|---|
| **What drives demand** | End-market tech cycles (PC, phone, auto, AI) and customer orders/forecasts | Patients: disease prevalence, diagnosis and treatment rates, prescriptions, payer coverage |
| **Volatility** | High and cyclical; boom/bust with a strong bullwhip | Commercial products fairly stable; big swings at launch, approval or label changes |
| **Big "events"** | New generation launch, end-of-life, shortage/glut cycles, export controls | Regulatory approval, launch curve, **loss of exclusivity / patent cliff**, generic and biosimilar entry |
| **Lead times** | About 3–6 months to make a chip [3]; a new leading-edge fab costs **$20B+** and takes **about 2–4 years** [17][18] | Long production and quality-release cycles. For vaccines (a type of biologic), **1–3 years**, with testing taking up to 70% of the time [19] |
| **Why inventory "dies"** | **Obsolescence** and ASP erosion: technology goes stale | **Expiry / shelf life**, cold chain, first-expiry-first-out (FEFO) picking |
| **Service-level philosophy** | Balance service against E&O risk; allocate in shortages | Very high, often around **98%+ on-time-in-full** for branded pharma [20], because a stockout can harm patients |
| **Pricing** | ASPs fall over the product's life | Mostly contracted and stable; gross-to-net deductions matter |
| **Regulation** | Export controls, tariffs, trade policy | GMP, FDA/EMA; in the U.S., the **DSCSA** requires serialised, electronically traceable prescription drug packages [21] |
| **Typical forecast method** | Customer/sales forecasts plus statistical/ML models, market intelligence and life-cycle curves | Patient-based (epidemiological) models, analog launch curves, tenders |
| **Key KPIs** | Book-to-bill, DOI, channel inventory, lead time, E&O | Forecast accuracy, days of supply, expiry write-offs, backorders |

**The shared core is what makes you transferable:**
- S&OP / IBP
- forecast accuracy and **bias** tracking
- safety-stock math
- ABC-XYZ segmentation
- Forecast Value Add

This project demonstrates all of them on semiconductor data. The same skills apply in biotech.

*One more link:* the M5 forecasting competition (Walmart sales, 2020) was won by an ensemble of **LightGBM** models, and gradient-boosted trees were common among top entries [22]. That's why LightGBM is in our model line-up.

---

## Sources
1. Bloomberg (2021-01-19), *A year of poor planning led to carmakers' massive chip shortage*: https://www.bloomberg.com/news/articles/2021-01-19/a-year-of-poor-planning-led-to-carmakers-massive-chip-shortage
2. CNBC (2021-02-08), *Carmakers have been hit hard by a global chip shortage*: https://www.cnbc.com/2021/02/08/carmakers-have-been-hit-hard-by-a-global-chip-shortage-heres-why-.html
3. Semiconductor Industry Association (2021): https://www.semiconductors.org/chipmakers-are-ramping-up-production-to-address-semiconductor-shortage-heres-why-that-takes-time/
4. Bloomberg (2021-08-10), *Chip delivery time surpasses 20 weeks*: https://www.bloomberg.com/news/articles/2021-08-10/chip-delivery-time-surpasses-20-weeks-in-no-sign-shortage-easing
5. The Register (2022-03-25): https://www.theregister.com/2022/03/25/chip_shortage_report
6. CNBC (2021-09-23), AlixPartners estimate: https://www.cnbc.com/2021/09/23/chip-shortage-expected-to-cost-auto-industry-210-billion-in-2021.html
7. CNBC (2021-04-28), Ford Q1 2021: https://www.cnbc.com/2021/04/28/ford-f-earnings-q1-2021.html
8. The Drive, unfinished Ford trucks at Kentucky Speedway: https://www.thedrive.com/news/40458/thousands-of-unfinished-ford-super-duty-trucks-are-parked-at-kentucky-speedway-due-to-chip-shortage
9. The Register (2022-05-26), inventory correction: https://www.theregister.com/2022/05/26/sharp_chip_inventory_correction_looms/
10. CNBC (2023-04-26), SK hynix record loss: https://www.cnbc.com/2023/04/26/sk-hynix-reports-record-quarterly-operating-loss-forecasts-better-outlook.html
11. Micron FQ2 2023 results (SEC 8-K): https://www.sec.gov/Archives/edgar/data/723125/000072312523000018/a2023q2ex991-pressrelease.htm
12. Manary, M. P. & Willems, S. P. (2008). Setting Safety-Stock Targets at Intel in the Presence of Forecast Bias. *Interfaces* 38(2):112–122. https://doi.org/10.1287/inte.1070.0339
13. HotHardware, Nvidia annual GPU cadence: https://hothardware.com/news/nvidia-roadmap-hints-annual-gpu-cadence
14. Intel product discontinuance notice example (PCN): https://cdrdv2-public.intel.com/799490/PCN119669-00.pdf
15. Tom's Hardware, TSMC on CoWoS constraint: https://www.tomshardware.com/news/tsmc-shortage-of-nvidias-ai-gpus-to-persist-for-15-years
16. SCMP / Reuters (2024), SK hynix HBM almost sold out: https://www.scmp.com/tech/big-tech/article/3261205/nvidia-supplier-sk-hynix-says-its-high-bandwidth-memory-chips-used-ai-processors-almost-sold-out
17. McKinsey, *Semiconductor design and manufacturing: achieving leading-edge capabilities*: https://www.mckinsey.com/~/media/McKinsey/Industries/Advanced%20Electronics/Our%20Insights/Semiconductor%20design%20and%20manufacturing%20Achieving%20leading%20edge%20capabilities/Semiconductor-design-and-manufacturing-Achieving-leading-edge-capabilities-v3.pdf
18. CNBC (2024-12-13), inside TSMC Arizona: https://www.cnbc.com/2024/12/13/inside-tsmcs-new-chip-fab-where-apple-will-make-chips-in-the-us-.html
19. Vaccines Europe, *How are vaccines produced*: https://www.vaccineseurope.eu/about-vaccines/how-are-vaccines-produced
20. McKinsey, *Outlook on pharma operations* (benchmark figures; dated ~2012–14): https://www.mckinsey.com/~/media/mckinsey/dotcom/client_service/operations/pdfs/outlook_on_pharma_operations.ashx
21. U.S. FDA, Drug Supply Chain Security Act: https://www.fda.gov/drugs/drug-supply-chain-integrity/drug-supply-chain-security-act-dscsa
22. Makridakis, Spiliotis & Assimakopoulos (2022). M5 accuracy competition: results, findings, and conclusions. *International Journal of Forecasting* 38(4). https://doi.org/10.1016/j.ijforecast.2021.11.013
