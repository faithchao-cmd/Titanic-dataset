import pandas as pd
df = pd.read_csv("data/raw/Titanic_messy_dataset.csv")

print("DATASET SHAPE:")
print(df.shape)

print("\nDATASET INFORMATION:")
df.info()

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nDUPLICATE ROWS:")
print(df.duplicated().sum())

# Drop duplicates
before = len(df)
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["PassengerId"], keep="first")
print(f"Removed {before - len(df)} duplicate rows")

# Standardized text casing/whitespace
df["Name"] = df["Name"].str.strip().str.title()

df["Sex"] = df["Sex"].str.strip().str.lower()
df["Sex"] = df["Sex"].replace({"m": "male", "f": "female"})

df["Embarked"] = df["Embarked"].str.strip().str.upper()
df["Embarked"] = df["Embarked"].replace({
    "SOUTHAMPTON": "S", "CHERBOURG": "C", "QUEENSTOWN": "Q"
})

df["Pclass"] = df["Pclass"].replace({"1st": 1, "2nd": 2, "3rd": 3})
df["Pclass"] = df["Pclass"].astype(int)

df["Survived"] = df["Survived"].replace({"Yes": 1, "Y": 1, "No": 0, "N": 0})
df["Survived"] = df["Survived"].astype(int)

# Fixed Fare (mixed symbols/units)
df["Fare"] = (
    df["Fare"].astype(str)
    .str.replace("$", "", regex=False)
    .str.replace("USD", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
)
df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce")

# Fixed Age (text with "yrs")
df["Age"] = (
    df["Age"].astype(str)
    .str.replace("yrs", "", regex=False)
    .str.strip()
)
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

# Fixed inconsistent dates
df["BookingDate"] = pd.to_datetime(df["BookingDate"], format="mixed")

# Handled nulls, case by case
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Embarked"] = df["Embarked"].fillna("Unknown")
df["Fare"] = df["Fare"].fillna(df.groupby("Pclass")["Fare"].transform("median"))
df["Cabin"] = df["Cabin"].fillna("Unknown")

# Verify after cleaning
print("\n--- AFTER CLEANING ---")
print("DATASET SHAPE (after):")
print(df.shape)

print("\nMISSING VALUES (after):")
print(df.isnull().sum())

print("\nDUPLICATE ROWS (after):")
print(df.duplicated().sum())

# Saved cleaned dataset
df.to_csv("data/cleaned/titanic_cleaned.csv", index=False)
print("\nSaved cleaned dataset to data/cleaned/titanic_cleaned.csv")