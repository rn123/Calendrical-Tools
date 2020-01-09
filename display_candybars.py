#!/usr/bin/env python
# coding: utf-8

import datetime
import json
from pathlib import Path

from jinja2 import Template
from tqdm import tqdm
import click

from candybar import pycalcal as pcc
from candybar import candybar as candybar


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

    return weeks


@click.command()
@click.option("--start", default=1, help="ISO week number.")
@click.option("--year", default=2020, help="The calendar year.")
def main(year=2020, start=None):
    year = int(year)
    cal = candybar.LaTeXCandyBar(year)
    new_moons = cal.new_moons
    wks = cal.wks
    iso = cal.iso

    gregorian_weeks = weeks_data(wks, new_moons=new_moons, calendar_type="gregorian")
    gregorian_tab = cal.prweeks(gregorian_weeks, new_moons)

    hebrew_weeks = weeks_data(wks, new_moons=new_moons, calendar_type="hebrew")
    hebrew_tab = cal.prweeks(hebrew_weeks, new_moons)

    islamic_weeks = weeks_data(wks, new_moons=new_moons, calendar_type="islamic")
    islamic_tab = cal.prweeks(islamic_weeks, new_moons)

    cache_file = "output/chinese_lunar_" + str(year)
    CACHE_FILE_EXISTS = False
    if Path(cache_file).exists():
        CACHE_FILE_EXISTS = True
        with open(cache_file) as fp:
            chinese_weeks = json.load(fp)
    else:
        chinese_weeks = weeks_data(wks, new_moons=new_moons, calendar_type="chinese")

    chinese_tab = cal.prweeks(chinese_weeks, new_moons)

    if CACHE_FILE_EXISTS is False:
        with open(cache_file, "w") as fp:
            json.dump(chinese_weeks, fp)

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

    with open("candybar/calendar_template.tex") as fd:
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

    outfile = "output/cal_" + str(year) + ".tex"
    with open(outfile, "w") as fp:
        fp.write(output)


if __name__ == "__main__":
    main()
