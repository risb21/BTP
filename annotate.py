import sys
import pandas as pd

COL1: str = "label"
COL2: str = "language"
COL3: str = "urgency"
FILE: str = "combined_dataset.csv"
CLASSES: dict[int, str] = {
    0: "Non-Complaint ",
    # -- Rest are complaints --
    1: "Delay",
    2: "Hygiene (food, toilets, carriage)",
    3: "Ticket issue (cancellation, refund, seat change)",
    4: "Medical issue",
    5: "Safety issue",
    6: "Travel Experience",
}
URGENCY: dict[int, str] = {
    0: "Low",
    1: "Pressing",
    2: "Critical",
}
LANG: dict[int, str] = {
    0: "English",
    1: "Hindi (devanagari; purely)",
    2: "Hinglish (devanagari; with english in latin alphabet)",
    3: "Hinglish (devanagari; with english transliterated to hindi)",
    4: "Hinglish (latin; with hindi transliterated to english)",
}

start: int = 0
df = pd.read_csv(FILE)
end: int = len(df)


TEMPLATE: str = f"""
================================================
Tweet #%d: "%s"

Categories:
{"\n".join(["%d -> %s" % (key, val) for key, val in CLASSES.items() if key >= 0])}
Urgency levels:
{", ".join(["%d -> %s" % (key, val) for key, val in URGENCY.items()])}
Language in tweet:
{"\n".join(["%d -> %s" % (key, val) for key, val in LANG.items()])}
================================================
"""

def save_exit() -> None:
    global df
    df.to_csv(FILE, index=False)
    print("Saved progress")
    sys.exit(0)

def main() -> None:
    global start, end, df
    df = pd.read_csv(FILE)
    end = len(df)
    while start <= end:
        if df.loc[start, COL1] < 0:
            break
        start += 1
    try:
        idx = start
        while idx < end:
            print(TEMPLATE % (idx, df.loc[idx, "SentimentText"],))

            try:
                label = int(input("Enter Category: "))
                lang = int(input("Enter Language of tweet: "))
            except ValueError:
                continue
            if label not in CLASSES or lang not in LANG:
                continue
            
            df.loc[idx, COL1] = label
            df.loc[idx, COL2] = lang

            # skip the rest if it is a garbage tweet or not a complaint
            if label <= 1:
                idx += 1
                continue

            try:
                urgency = int(input("Enter urgency level: "))
            except ValueError:
                continue
            if urgency not in URGENCY:
                continue

            df.loc[idx, COL3] = urgency

            idx += 1
    except KeyboardInterrupt:
        save_exit()

    save_exit()
    
    
if __name__ == "__main__":
    main() 