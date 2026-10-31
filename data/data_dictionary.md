# Data dictionary

Unit: individual assigned customer, as documented by the publisher. No customer ID exists. Original field names and category spellings are retained.

| Field | Role | Meaning / validation |
|---|---|---|
| recency | Pretreatment | Integer months since last purchase, 1–12 |
| history | Pretreatment | Prior-year dollar spending, nonnegative |
| history_segment | Pretreatment | Publisher's seven spending bands, $0–100 through $1,000+ |
| mens | Pretreatment | Purchased men's merchandise in prior year, 0/1; not customer gender |
| womens | Pretreatment | Purchased women's merchandise in prior year, 0/1; not customer gender |
| zip_code | Pretreatment | Urban / Surburban / Rural (original misspelling preserved) classification; no exact postcode |
| newbie | Pretreatment | New customer in prior twelve months, 0/1 |
| channel | Pretreatment | Phone / Web / Multichannel historical purchase channel |
| segment | Assignment | No E-Mail / Mens E-Mail / Womens E-Mail |
| visit | Secondary outcome | Website visit in following two weeks, 0/1 |
| conversion | Primary outcome | Purchase in following two weeks, 0/1 |
| spend | Secondary outcome | Dollars spent in following two weeks, includes zeros |

Rates use all assigned customers as denominators. Absolute binary differences are probabilities (multiply by 100 for percentage points). Relative lift = (treatment mean − reference mean) / reference mean, undefined if reference mean is zero. Spending is never averaged over purchasers alone in the main analysis. All preprocessing is validated but no source observations are removed or altered. No dates, opens, clicks or customer demographics are inferred.
