# Titanic Dataset — Data Cleaning and Processing

## Description
This project cleans and prepares a raw Titanic-style passenger dataset containing
null values, duplicate rows, inconsistent formats, and incorrect data types, so
that it is ready for reliable analysis.

## Objective
Identify and fix common data quality issues in a raw dataset using Python and
pandas, and document each fix so the process is transparent and reproducible.

## Tools
- Python
- Pandas
- VS Code / GitHub Codespaces

## Project Structure
```
Titanic-dataset/
├── data/
│   ├── raw/          # original, unmodified dataset
│   └── cleaned/       # cleaned output dataset
├── docs/
│   └── cleaning_report.txt   # before/after inventory checks (auto-generated)
├── notes/
│   └── data_cleaned.py       # cleaning script
├── screenshots/
└── README.md
```


## Data Quality Issues Found and How Each Was Resolved

| # | Issue | Column(s) Affected | Resolution |
|---|-------|--------------------|------------|
| 1 | Duplicate rows (exact and near-duplicate entries, some reused PassengerIds) | All / `PassengerId` | Removed exact duplicates with `drop_duplicates()`; removed duplicate `PassengerId` entries, keeping the first occurrence |
| 2 | Inconsistent text casing and stray whitespace | `Name`, `Sex` | Stripped whitespace and standardized casing (`.str.strip()`, `.str.title()` / `.str.lower()`); collapsed shorthand values (`m`, `f`, `M`, `F`) into `male` / `female` |
| 3 | Inconsistent category labels | `Embarked` | Standardized to uppercase single-letter codes (`S`, `C`, `Q`); mapped full port names (e.g. "Southampton") back to their codes |
| 4 | Mixed data types stored as text | `Pclass`, `Survived` | Mapped text values (`"1st"`, `"Yes"`, `"Y"`, etc.) back to their correct numeric/int representations |
| 5 | Numbers stored as inconsistent text with mixed units/symbols | `Fare` | Stripped `$` and `USD`; converted comma decimal separators to periods; converted the column to numeric with `pd.to_numeric()` |
| 6 | Numbers stored as text with units attached | `Age` | Removed the `"yrs"` suffix and converted to numeric |
| 7 | Inconsistent date formats (4 different formats present) | `BookingDate` | Parsed all formats using `pd.to_datetime(..., format="mixed")` into a single consistent datetime format |
| 8 | Missing values | `Age`, `Embarked`, `Fare`, `Cabin` | Handled case by case rather than one blanket method — see below |

### Null-Handling Decisions
Each column's missing values were treated differently based on the type and
extent of missingness, per the assignment's guidance to avoid a one-size-fits-all approach:

- **Age** — numeric, moderate missingness → imputed with the median age.
- **Fare** — numeric, few missing values → imputed with the median fare within the
  same passenger class, since fare correlates strongly with class.
- **Embarked** — categorical, very few missing values → flagged as `"Unknown"`
  rather than guessed, to avoid introducing inaccurate assumptions.
- **Cabin** — mostly missing and not missing at random (strongly tied to
  passenger class) → flagged as `"Unknown"` rather than dropped, to preserve
  the rest of each row's data.

## Verification
After cleaning, the same inventory checks used at the start
(`df.info()`, `df.isnull().sum()`, `df.duplicated().sum()`) were re-run to
confirm:
- 0 remaining duplicate rows
- 0 remaining unexpected missing values (aside from intentionally flagged `"Unknown"` entries)
- All columns hold the correct data type (numeric columns are numeric, dates are datetime)

Full before/after output is available in [`docs/cleaning_report.txt`](docs/cleaning_report.txt).

## Deliverables
- Cleaned dataset: `data/cleaned/titanic_cleaned.csv`
- Cleaning script: `notes/data_cleaned.py`
- Before/after inventory report: `docs/cleaning_report.txt`
- This README, summarizing issues found and how each was resolved

## Notes
This dataset is a synthetic, Titanic-style dataset generated for practicing
data cleaning techniques. It is not the original public Titanic dataset.
