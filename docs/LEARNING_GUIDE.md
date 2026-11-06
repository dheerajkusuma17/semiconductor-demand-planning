# Learning Guide & Interview Prep

This is your personal study document. It grows with every `/checkpoint`: each phase adds its checkpoint questions, your answers, model answers, and interview-style follow-ups.

## How to use it before an interview
1. Read each phase's model answers out loud. Can you explain each one in under a minute, without notes?
2. Practise the "Interview follow-up" questions with a friend, or ask Claude to role-play the interviewer.
3. For each number on your resume, know **where it came from** (which notebook, which metric, which data).

## Excel → Python cheat sheet
| You know this in Excel | In pandas (Python) |
|---|---|
| Open a file | `pd.read_csv("file.csv")` / `pd.read_excel("file.xlsx")` |
| AutoFilter | `df[df["SKU"] == "SKU-A-2"]` |
| Sort | `df.sort_values("Week")` |
| New column with a formula | `df["Error"] = df["Forecast"] - df["Actual"]` |
| PivotTable | `df.pivot_table(index="SKU", columns="DC", values="Orders", aggfunc="sum")` |
| SUMIFS / group subtotal | `df.groupby("SKU")["Orders"].sum()` |
| XLOOKUP / VLOOKUP | `df.merge(lookup_df, on="SKU", how="left")` |
| Moving-average column | `df["Orders"].rolling(4).mean()` |
| Previous row's value | `df["Orders"].shift(1)` |
| `NORM.S.INV(0.95)` | `scipy.stats.norm.ppf(0.95)` |
| `IFERROR` | `df["x"].fillna(0)` |
| Line chart | `df.plot(x="Week", y="Orders")` |

---

<!-- Phase entries are appended below by /checkpoint -->
