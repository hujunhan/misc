import pandas as pd

csv_path = "/Users/hu/Downloads/metadata_all.csv"  # change this

df = pd.read_csv(csv_path)

df_target = df.copy()

print("Total target photos:", len(df_target))


def parse_focal(s):
    if isinstance(s, str) and "mm" in s:
        try:
            return float(s.split()[0])
        except ValueError:
            return None
    return None


df_target["FocalLength_mm"] = df_target["FocalLengthIn35mmFormat"].apply(parse_focal)

# Overall summary
print(df_target["FocalLength_mm"].describe())

# Top 20 exact focal lengths (rounded to 1 decimal)
print(df_target["FocalLength_mm"].round(1).value_counts().head(20))

# Top 20 camera models
print(df_target["Model"].value_counts().head(20))

# save df as compressed format
