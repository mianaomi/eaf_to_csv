import csv 
import pympi # this is a special package, use pip install pympi-ling to set up coding enviornment
import tkinter as tk # this is usually already installed but it's a similar thing: if you don't have it, install w/ pip
from tkinter import filedialog
# run as python eaf_to_csv.py in terminal

# this function takes an eaf file path and converts it to a list of rows
# we assume tiers are aligned by annotation index (aka start time)
# if a tier has fewer annotations than others we fill missing cells with blanks/null

def eaf_to_csv(eaf_path):
    # load eaf file
    eaf = pympi.Elan.Eaf(eaf_path)
    
    # get tier names and remove default
    tiers = [t for t in eaf.tiers.keys() if t.lower() != "default"]

    # build data for each tier including start times and texts
    tier_data = {}
    max_len = 0
    for tier in tiers:
        anns = eaf.get_annotation_data_for_tier(tier)
        starts = [a[0] for a in anns]
        texts = [a[2] for a in anns]
        tier_data[tier] = list(zip(starts, texts))
        if len(anns) > max_len:
            max_len = len(anns)

    # make headers- each tier gets two columns
    headers = ["start_time"]
    for tier in tiers:
        headers.append(f"{tier}_text")

    # build rows aligned by index (in this case start) -- functionally SELF JOIN
    rows = []
    for i in range(max_len):
        row = {}
        # take start from first tier
        if i < len(tier_data[tiers[0]]):
            row["start_time"] = tier_data[tiers[0]][i][0]
        else:
            row["start_time"] = ""
            
        for tier in tiers:
            if i < len(tier_data[tier]):
                _, text = tier_data[tier][i]
                row[f"{tier}"] = text
            else:
                row[f"{tier}"] = ""
        rows.append(row)

    return headers, rows

# this function saves rows to a csv file

def save_csv(headers, rows):
    root = tk.Tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("csv files", "*.csv")],
        title="save csv as"
    )
    if save_path:
        with open(save_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        print("csv saved at", save_path)
    else:
        print("save cancelled")

# driver
if __name__ == "__main__":
    # prompt user to paste eaf file path, you can copy this from a shift+right click on pc, use CTRL+V
    eaf_path = input("copy paste path to your eaf file, remove surround quotes: ").strip().strip('"').strip("'") 
    if eaf_path: # convert and save
        headers, rows = eaf_to_csv(eaf_path)
        save_csv(headers, rows)
    else:
        print("no file path entered")



