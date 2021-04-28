import pandas as pd
from tika import parser
import re
import os


days_of_week = {"MWF": ["0", "2", "4"],
                "MW": ["0", "2"],
                "F": ["4"],
                "W": ["2"],
                "TR": ["1", "3"],
                "TTh": ["1", "3"],}

formats = ["(\s[A-Z][A-Z][A-Z]\s\d\d:\d\d[ ]?–[ ]?\d\d:\d\d)",
           "(\s[A-Z][A-Z][a-z]\s\d\d:\d\d[ ]?–[ ]?\d\d:\d\d)",
           "(\s[A-Z][A-Z]\s\d\d:\d\d[ ]?–[ ]?\d\d:\d\d)",
           "(\s[A-Z]\s\d\d:\d\d[ ]?–[ ]?\d\d:\d\d)"]


def fill_table(oh, lh):
    os.remove("templates/template_5days_filled.csv")

    df = pd.read_csv("templates/template_5days.csv")
    df["CLASS 1"] = ""

    for h in oh:
        weekday = int(h.split(" ")[1])
        for i, row in df.iterrows():
            if i % 5 == weekday and row["Day Done?"] == 0.0:
                df.loc[df["Date"] == row.Date, "CLASS 1"] += "Office Hours [{}]".format(" ".join(h.split(" ")[2:5]))

    for h in lh:
        weekday = int(h.split(" ")[1])
        for i, row in df.iterrows():
            if i % 5 == weekday and row["Day Done?"] == 0.0:
                df.loc[df["Date"] == row.Date, "CLASS 1"] += "Lecture [{}]; ".format(" ".join(h.split(" ")[2:5]))

    df.to_csv("templates/template_5days_filled.csv")
    return "templates/template_5days_filled.csv"


def get_hours(file):
    raw = parser.from_file(file)
    days_of_week = {"MWF": ["0", "2", "4"],
                    "MW": ["0", "2"],
                    "F": ["4"],
                    "W": ["2"],
                    "TR": ["1", "3"],
                    "TTh": ["1", "3"],}

    office_hours, lecture_hours = "", ""

    for line in raw["content"].split("\n"):
        line = line.replace("-", "–")
        if "office" in line.lower():
            for f in formats:
                if len(re.findall(f, line)) > 0:
                    office_hours = re.findall(f, line)[0]
                    break

        if "lecture" in line.lower():
            for f in formats:
                if len(re.findall(f, line)) > 0:
                    lecture_hours = re.findall(f, line)[0]
                    break
        if len(lecture_hours) > 0 and len(office_hours) > 0:
            break

    lh, oh = [], []
    for k, v in days_of_week.items():
        if k in lecture_hours:
            for value in v:
                lh.append(lecture_hours.replace(k, value))

            break
    for k, v in days_of_week.items():
        if k in office_hours:
            for value in v:
                oh.append(office_hours.replace(k, value))

    return oh, lh