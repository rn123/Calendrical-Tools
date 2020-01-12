#!/usr/bin/env python
# coding: utf-8

import datetime
import json
from pathlib import Path

from jinja2 import Template
from tqdm import tqdm
import click

from pycalcal import pycalcal as pcc
from calendrical_tools import candybar


from_fixed_functions = {
    "gregorian": pcc.gregorian_from_fixed,
    "hebrew": pcc.hebrew_from_fixed,
    "islamic": pcc.islamic_from_fixed,
    "chinese": pcc.chinese_from_fixed,
}

template_text = r"""
\documentclass[9pt, landscape]{article}
\usepackage{calc, layouts, graphicx, wasysym, multirow, array}
\usepackage[lmargin=40pt, tmargin=40pt, bmargin=0pt]{geometry}
\pagestyle{empty}
\begin{document}

\resizebox{!}{9cm}{
    \begin{tabular}{|c|c|c|c|c|}
        \hline
        Gregorian & Lunar & Hebrew & Islamic & Chinese \\
        {{ year_display -}}  \\
        \hline
        {{ gregorian_data }} &
        {{ lunar_data }}     &
        {{ hebrew_data }}    &
        {{ islamic_data }}   &
        {{ chinese_data }}   \\
        \hline
    \end{tabular}
    }
\end{document}"""

template = Template(template_text)


@click.command()
@click.option("--start", default=1, help="ISO week number.")
@click.option("--year", default=2020, help="The calendar year.")
def main(year=2020, start=None):
    year = int(year)
    cal = candybar.LaTeXCandyBar(year)
    new_moons = cal.new_moons

    formatted_weeks = []
    for w in cal.weeks["gregorian"]:
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
        gregorian_data=cal.prweeks(cal.weeks["gregorian"], new_moons),
        lunar_data=lunar_tab,
        hebrew_data=cal.prweeks(cal.weeks["hebrew"], new_moons),
        islamic_data=cal.prweeks(cal.weeks["islamic"], new_moons),
        chinese_data=cal.prweeks(cal.weeks["chinese"], new_moons),
    )

    outfile = "output/cal_" + str(year) + ".tex"
    with open(outfile, "w") as fp:
        fp.write(output)


if __name__ == "__main__":
    main()
