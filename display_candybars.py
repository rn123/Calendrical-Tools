#!/usr/bin/env python
# coding: utf-8

import datetime
import json
from pathlib import Path

from jinja2 import Template
from tqdm import tqdm

from candybar import pycalcal as pcc
from candybar import candybar as candybar

# Brute force way to get a list of new moons occuring during the year. First
# approximate the number of new moons since the year 0 (using simple
# observation that length of month alternates between 29 and 30 days). Use
# astronomical approximation to get precise dates of new moons in the year.


def many_moons(fixed_date, epoch=0):
    # Use part of formula for islamic_from_fixed:
    # year = quotient(30 * (date - ISLAMIC_EPOCH) + 10646, 10631)
    # but replace ISLAMIC_EPOCH with and epoch of 0 to approximate the
    # number of new moons since the epoch.
    # TODO: grok the cycle of leap year formula behind this approximation.
    year = pcc.quotient(30 * (fixed_date - epoch) + 10646, 10631)
    no_moons = year * 12
    return no_moons


def new_moons_in_year(year):
    fixed_date = pcc.fixed_from_gregorian([year, 1, 1])
    no_moons = many_moons(fixed_date)
    moon_rng = range(no_moons - 12, no_moons + 13)
    new_moons_data = [(n, pcc.nth_new_moon(n)) for n in moon_rng]
    new_moons = {}
    for n, nnm in new_moons_data:
        nm = pcc.gregorian_from_fixed(nnm)
        key = int(nnm)
        new_moons[key] = (n, nm, nnm)

    return new_moons


from_fixed_functions = {
    "gregorian": pcc.gregorian_from_fixed,
    "hebrew": pcc.hebrew_from_fixed,
    "islamic": pcc.islamic_from_fixed,
    "chinese": pcc.chinese_from_fixed,
}


def chinese_day(d):
    return pcc.chinese_day(from_fixed_functions["chinese"](d))


def standard_day(d, calendar_type="gregorian"):
    return pcc.standard_day(from_fixed_functions[calendar_type](d))


def weeks_data(wks, new_moons=None, calendar_type="gregorian"):
    weeks = []
    cache_file = "chinese_lunar_2020"
    CACHE_FILE_EXISTS = False
    if Path(cache_file).exists() and (calendar_type == "chinese"):
        CACHE_FILE_EXISTS = True
        with open(cache_file) as fp:
            weeks = json.load(fp)
    else:
        for w in tqdm(wks):
            iso_week_number = pcc.iso_week(pcc.iso_from_fixed(w[0][0]))
            week_data = {}
            week_data["iso"] = iso_week_number
            week_data["raw"] = w
            for d in w:
                if d[0] in new_moons:
                    new_moon = from_fixed_functions[calendar_type](d[0])
                    week_data["new_moon"] = new_moon
                    week_data["new_moon_fixed"] = d[0]
            week = [week_data]
            if calendar_type == "chinese":
                week.append([chinese_day(d[0]) for d in w])
            else:
                week.append([standard_day(d[0], calendar_type) for d in w])
            weeks.append(week)

    if (CACHE_FILE_EXISTS is False) and (calendar_type == "chinese"):
        with open(cache_file, "w") as fp:
            json.dump(weeks, fp)

    return weeks


def main(year=2020):
    cal = candybar.LaTeXCandyBar()
    new_moons = new_moons_in_year(year)
    wks, iso = cal.isoweeks(year)

    gregorian_weeks = weeks_data(wks, new_moons=new_moons, calendar_type="gregorian")
    gregorian_tab = cal.prweeks(gregorian_weeks, new_moons)

    hebrew_weeks = weeks_data(wks, new_moons=new_moons, calendar_type="hebrew")
    hebrew_tab = cal.prweeks(hebrew_weeks, new_moons)

    islamic_weeks = weeks_data(wks, new_moons=new_moons, calendar_type="islamic")
    islamic_tab = cal.prweeks(islamic_weeks, new_moons)

    chinese_weeks = weeks_data(wks, new_moons=new_moons, calendar_type="chinese")
    chinese_tab = cal.prweeks(chinese_weeks, new_moons)

    formatted_weeks = []
    for w in gregorian_weeks:
        output = ""
        if "new_moon" in w[0]:
            i = w[0]["new_moon_fixed"]
            moments = pcc.clock_from_moment(new_moons[i][2])[0:2]
            ts = ":".join(str(t) for t in moments)
            output += r"{}".format(ts)
        else:
            output += ""
        formatted_weeks.append(output)

    lunar_template_text = r"""\begin{tabular}{c}
    {% for w in weeks -%}
        {{ w }} \\
    {%- endfor %}
    \end{tabular}"""
    lunar_template = Template(lunar_template_text)
    lunar_tab = lunar_template.render(weeks=formatted_weeks)

    with open("calendar_template.tex") as fd:
        template_text = fd.read()
    template = Template(template_text)

    # Hebrew calendar year
    hstart = pcc.standard_year(
        pcc.hebrew_from_fixed(pcc.fixed_from_gregorian([year, 1, 1]))
    )
    hend = pcc.standard_year(
        pcc.hebrew_from_fixed(pcc.fixed_from_gregorian([year, 12, 1]))
    )

    # Islamic calendar year
    istart = pcc.standard_year(
        pcc.islamic_from_fixed(pcc.fixed_from_gregorian([year, 1, 1]))
    )
    iend = pcc.standard_year(
        pcc.islamic_from_fixed(pcc.fixed_from_gregorian([year, 12, 1]))
    )

    year_display = r"{}& Phases & {}/{}& {}/{}&{}".format(
        year, hstart, hend, istart, iend, year
    )

    output = template.render(
        year_display=year_display,
        gregorian_data=gregorian_tab,
        lunar_data=lunar_tab,
        hebrew_data=hebrew_tab,
        islamic_data=islamic_tab,
        chinese_data=chinese_tab,
    )

    with open("cal.tex", "w") as fp:
        fp.write(output)


if __name__ == "__main__":
    main(2020)
