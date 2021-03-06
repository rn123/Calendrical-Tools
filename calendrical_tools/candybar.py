#!/usr/bin/env python
# coding: utf-8

import datetime
import json
from pathlib import Path
from collections import namedtuple

from jinja2 import Template
from tqdm import tqdm
import click

from pycalcal import pycalcal as pcc

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


class CandyBar:
    firstweekday = 0

    def __init__(self, year=2020, weeks_before=1, weeks_after=0):
        self.year = year
        self._wks_before = weeks_before
        self._wks_after = weeks_after

        wks, iso = self.isoweeks(
            year, weeks_before=self._wks_before, weeks_after=self._wks_after
        )
        self._wks = wks
        self.iso = iso
        self.new_moons = self.new_moons_in_year(year)
        self.weeks = {}

        self.cache_file = "output/chinese_lunar_" + str(year)
        self.CACHE_FILE_EXISTS = False

        for calendar_type in ["gregorian", "islamic", "hebrew", "chinese"]:
            if (calendar_type == "chinese") and Path(self.cache_file).exists():
                self.CACHE_FILE_EXISTS = True
                with open(self.cache_file) as fp:
                    self.weeks["chinese"] = json.load(fp)
            else:
                self.weeks[calendar_type] = self.weeks_data(
                    wks=self._wks, new_moons=self.new_moons, calendar_type=calendar_type
                )

            if (calendar_type == "chinese") and (self.CACHE_FILE_EXISTS is False):
                with open(self.cache_file, "w") as fp:
                    json.dump(self.weeks["chinese"], fp)

    #     def itersolar(self, start, end):
    #          # Assumption: cal=calendar.CandyBar(6) <-- 1st day of week is Sunday.
    #          daymap = {'6':'1', '0':'2','1':'3','2':'4','3':'5','4':'6','5':'7'}
    #          year = start
    #          while True:
    #               firstday = daymap[str(calendar.weekday(year, 1, 1))]
    #               if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
    #                    firstday = firstday + 'L'
    #                    yield [year, firstday]
    #                    year += 1
    #                    if year == end: break

    def iteroddfridays(self, year, month):
        date = datetime.date(year, month, 1)
        days = (date.weekday() - self.firstweekday) % 7
        date -= datetime.timedelta(days=days)
        for i in range(0, 6):
            if date.weekday() == 4:
                break
            date += datetime.timedelta(days=1)
            saturday = date + datetime.timedelta(days=1)
            sunday = date + datetime.timedelta(days=2)
            if saturday.day == 1 or sunday.day == 1:
                date += datetime.timedelta(days=7)
                twoweeks = datetime.timedelta(days=14)
            while True:
                yield date
                date += twoweeks
            if date.month != month:
                break

    def isoweeks(self, year, weeks_before=1, weeks_after=0):
        """
        ISO weeks determined by nth Thursdays.
        """
        ## Use pycalcal to find first Thursday of the year. Returns an integer
        ## day count of days elapsed since 1/1/1 (rata die -- fixed day).
        first_thursday = pcc.nth_kday(1, 4, [year, 1, 1])
        ## Back up and enumerate days starting the week before.
        days = [
            first_thursday - 3 - (7 * weeks_before) + j
            for j in range(0, (53 + weeks_before + weeks_after) * 7)
        ]
        days_dates = [(d, pcc.gregorian_from_fixed(d)) for d in days]
        ## List of weeks, starting on Mondays
        weeks = [days_dates[i : i + 7] for i in range(0, len(days_dates), 7)]

        ## Count weeks (actually starting Mondays) in each month.
        iso = dict()
        iso_list = []
        for w in weeks:
            # Key is the year and month of the starting Monday.
            key = (
                str(pcc.standard_year(w[0][1])) + "_" + str(pcc.standard_month(w[0][1]))
            )
            if key not in iso:
                iso[key] = 1
            else:
                iso[key] += 1
        ## A dictionary was used to accumulate count. Now create sorted list of
        ## months with count of how many iso weeks (Mondays) start in that month.
        for k in iso:
            pair = list(map(int, k.split("_")))
            iso_list.append([pair[0], pair[1], iso[k]])
            iso_list.sort()
        return (weeks, iso_list)

    def iteryeardates(self, year):
        """
        Return an iterator for one year. The iterator will yield datetime.date
        values and will always iterate through complete weeks, so it will yield
        dates outside the specified year.
        """
        date = datetime.date(year, 1, 1)
        # Go back to the beginning of the week
        days = (date.weekday() - self.firstweekday) % 7
        date -= datetime.timedelta(days=days)
        oneday = datetime.timedelta(days=1)
        while True:
            yield date
            date += oneday
            if date.year != year and date.weekday() == self.firstweekday:
                break

    def iteryeardays2(self, year):
        """
        Like iteryeardates(), but will yield (day number, weekday number)
        tuples. For days outside the specified month the day number is 0.
        """
        for date in self.iteryeardates(year):
            if date.year != year:
                yield (0, date.weekday())
            else:
                yield (date.day, date.weekday())

    def iterHebrewYearDates(self, year):
        """
        Return an iterator for one year. The iterator will yield Hebrew dates
        corresponding to the gregorian year and will always iterate
        through complete weeks, so it will yield dates outside the specified year.
        """
        date = datetime.date(year, 1, 1)
        # Go back to the beginning of the week
        days = (date.weekday() - self.firstweekday) % 7
        date -= datetime.timedelta(days=days)
        oneday = datetime.timedelta(days=1)
        while True:
            yield pcc.hebrew_from_fixed(
                pcc.fixed_from_gregorian([date.year, date.month, date.day])
            )
            date += oneday
            if date.year != year and date.weekday() == self.firstweekday:
                break

    def iteryeardays2_Hebrew(self, year, cal_type):
        """
        Like iteryeardates(), but will yield (day number, weekday number)
        tuples. For days outside the specified month the day number is 0.
        """
        for date in self.iteryeardates(year):
            if date.year != year:
                fd = pcc.fixed_from_gregorian([date.year, date.month, date.day])
                d = pcc.hebrew_from_fixed(fd)
                day_value = pcc.standard_day(d)
                month_value = pcc.standard_month(d)
                year_value = pcc.standard_year(d)
                yield [(0, date.weekday()), (year_value, month_value)]
            else:
                fd = pcc.fixed_from_gregorian([date.year, date.month, date.day])
                if cal_type == "hebrew":
                    d = pcc.hebrew_from_fixed(fd)
                    day_value = pcc.standard_day(d)
                    month_value = pcc.standard_month(d)
                    year_value = pcc.standard_year(d)
                elif cal_type == "chinese":
                    d = pcc.chinese_from_fixed(fd)
                    day_value = pcc.chinese_day(d)
                    month_value = pcc.chinese_month(d)
                else:
                    print("type %s not implemented" % cal_type)
                    return
                    yield [(day_value, date.weekday()), (year_value, month_value)]

    def iteryeardays3(self, year):
        """
        Like iteryeardates(), but will yield (day number, weekday number)
        tuples. For days outside the specified month the day number is 0.
        """
        #          odd_fridays = [f for m in range(1,13) for f in self.iteroddfridays(year,m)]
        for date in self.iteryeardates(year):
            if date.year != year:
                yield (0, date.weekday())
            else:
                yield (date.day, date.weekday())

    # Brute force way to get a list of new moons occuring during the year. First
    # approximate the number of new moons since the year 0 (using simple
    # observation that length of month alternates between 29 and 30 days). Use
    # astronomical approximation to get precise dates of new moons in the year.

    def many_moons(self, fixed_date, epoch=0):
        # Use part of formula for islamic_from_fixed:
        # year = quotient(30 * (date - ISLAMIC_EPOCH) + 10646, 10631)
        # but replace ISLAMIC_EPOCH with and epoch of 0 to approximate the
        # number of new moons since the epoch.
        # TODO: grok the cycle of leap year formula behind this approximation.
        year = pcc.quotient(30 * (fixed_date - epoch) + 10646, 10631)
        no_moons = year * 12
        return no_moons

    def new_moons_in_year(self, year):

        new_moon_tuple = namedtuple(
            "new_moon_tuple",
            "moon_since_1_1, moon_gregorian_date, moon_fixed_day, moon_sidereal_longitude",
        )
        fixed_date = pcc.fixed_from_gregorian([year, 1, 1])
        fudge_factor = 3
        no_moons = self.many_moons(fixed_date)
        moon_rng = range(
            no_moons - 12 - (4 * self._wks_before + fudge_factor),
            no_moons + 13 + (4 * self._wks_after + fudge_factor),
        )
        new_moons_data = [(n, pcc.nth_new_moon(n)) for n in moon_rng]
        new_moons = {}
        for n, nnm in new_moons_data:
            nm = pcc.gregorian_from_fixed(nnm)
            key = int(nnm)
            new_moons[key] = new_moon_tuple(
                moon_since_1_1=n,
                moon_gregorian_date=nm,
                moon_fixed_day=nnm,
                moon_sidereal_longitude=pcc.sidereal_lunar_longitude(nnm),
            )
        return new_moons

    def weeks_data(self, wks=None, new_moons=None, calendar_type="gregorian"):
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

    def candybar(self, year):
        days = [d for d in self.iteryeardays3(year)]
        return [days[i : i + 7] for i in range(0, len(days), 7)]


class TextCandyBar(CandyBar):
    def formatday(self, day, weekday, width):
        """
        Returns a formatted day.
        """
        if day == 0:
            s = ""
        else:
            s = "%02i" % day  # right-align single-digit days
        return s.center(width)

    def formatweek(self, week):
        nm = ""
        if "new_moon" in week:
            nm = week["new_moon"][2]
        formatted_days = [
            "{:2}".format("NM" if d[2] == nm else d[2]) for m, d in week["raw"]
        ]
        formatted_week = " ".join(formatted_days)
        formatted_week = formatted_week.replace(" 0", "  ")
        return formatted_week

    def prcandybar(self):
        for w in self.weeks["gregorian"]:
            print("{:2}".format(w[0]["iso"]) + "\t" + self.formatweek(w[0]))

    def prhebrewcandybar(self, year):
        days = [d for d in self.iteryeardays2_Hebrew(year)]
        weeks = [days[i : i + 7] for i in range(0, len(days), 7)]
        for w in weeks:
            print(self.formatweek(w))


class SvgCandyBar(CandyBar):
    boilerplate = """
    <svg style="border:1px solid black;" 
        viewbox="0 0 {{ width }} {{ height }}" 
        width="{{ width }}" height="{{ height }}" 
        xmlns="http://www.w3.org/2000/svg" 
        xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" 
        xmlns:xlink="http://www.w3.org/1999/xlink">

    <g id="candybar">
        <title>SVG CandyBar</title>
        <defs>
            <style type="text/css">
                #iso {
                    font-family: Courier, Arial, Helvetica, sans-serifArial, Helvetica, sans-serif;  
                    font-size: 15px;
                    font-weight: normal;
                    fill: {{ cal_color.iso }};
                    text-anchor: end;
                }
                #cal_dim {
                    font-family: Courier, Arial, Helvetica, sans-serif;  
                    font-size: 15px;
                    font-weight: normal;
                    fill: {{ cal_color.dim }};
                    text-anchor: end;
                }
                #cal_highlight {
                    font-family: Courier, Arial, Helvetica, sans-serif;  
                    font-size: 15px;
                    font-weight: normal;
                    fill: {{ cal_color.highlight }};
                    text-anchor: end;
                }
                #cal_highlight_bold {
                    font-family: Courier, Arial, Helvetica, sans-serif;  
                    font-size: 15px;
                    font-weight: bold;
                    fill: {{ cal_color.highlight_bold }}
                    text-anchor: end;
                }
                #cal_background {
                    fill: {{ cal_color.background }}
                }
            </style>
        </defs>
        
        {% for bar in bars %}
            <g transform="translate{{ bar.x, 20 }}">
                {{ bar.svg }}
            </g>
        {% endfor %}
    </g>
    </svg>
    """

    bar_template = """
    <g>
        <title>Calendar</title>
        <text x="{{ bar_width / 2.0 }}" y="0" text-anchor="middle">{{ bar_heading }}</text>
        {% for line in lines %}
            <text y="{{ loop.index * 1.1 }}em">
            {% for word in line.week %}
                <tspan id="{{ word.tag }}" x="{{ loop.index * 1.5 }}em">{{ word.day }}</tspan>
            {% endfor %}
            </text>
        {% endfor %}
    </g>
    """

    # colors to help debug layouts
    cal_color = {
        "iso": "lightgrey",
        "dim": "grey",
        "highlight": "green",
        "highlight_bold": "red",
        "background": "yellow",
    }

    def __init__(self):
        super().__init__()
        self.bar_heading = self.year

    def bar_data(self, cal_type="gregorian"):
        cal_data = []
        iso_list = [w[0]["iso"] for w in self.weeks[cal_type]]
        y_select = [2020]
        m_select = [1, 2]
        #     m_select = list(range(1,13))
        #     w_select = iso_list
        w_select = [4, 5, 6, 7, 8]
        d_number_select = list(range(25, 32)) + list(range(1, 22))
        for w in self.weeks[cal_type]:
            week = {"iso": w[0]["iso"], "week": []}
            for d, d_number in zip(w[0]["raw"], w[1]):
                y = d[1][0]
                m = d[1][1]
                dn = d[1][2]
                iso_number = w[0]["iso"]
                if ((m == 1) and (dn in list(range(25, 32)))) or (
                    m == 2 and dn in list(range(1, 23))
                ):
                    tag = "cal_highlight"
                else:
                    tag = "cal_dim"
                day = {"day": d_number, "tag": tag}
                week["week"].append(day)
            cal_data.append(week)

        return cal_data

    def prcandybar(self):
        bars = []
        bar_width = 200

        iso_list = [w[0]["iso"] for w in self.weeks["gregorian"]]
        iso_data = [
            {"iso": iso, "week": [{"day": iso, "tag": "iso"}]} for iso in iso_list
        ]

        for cal_type in ["gregorian", "chinese"]:
            cal_data = self.bar_data(cal_type)
            template = Template(self.bar_template)
            svg_bar = template.render(
                lines=cal_data, year=self.year, bar_width=bar_width
            )
            bars.append({"width": bar_width, "svg": svg_bar})

        template = Template(self.bar_template)
        svg_bar = {
            "x": 180,
            "width": 20,
            "svg": template.render(lines=iso_data, year="", bar_width=20),
        }

        bars[0]["x"] = 10
        bars[1]["x"] = 220
        all_bars = [bars[0], svg_bar, bars[1]]

        template = Template(self.boilerplate)
        self.svg = template.render(
            bars=all_bars, width=400, height=750, cal_color=self.cal_color
        )


class LaTeXCandyBar(CandyBar):
    months = {
        "gregorian": [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        "hebrew": [
            "Nisan",
            "Iyyar",
            "Sivan",
            "Tammuz",
            "Av",
            "Elul",
            "Tishri",
            "Marheshvan",
            "Kislev",
            "Tevet",
            "Shevat",
            "Adar",
            "Adar II",
        ],
    }

    candybar_template_text = r"""
    \begin{tabular}{l|ccccccc|rr}
        {% for w in weeks -%} 
            {{ w }}
        {%- endfor %} 
    \end{tabular}"""

    def formatmonthnames(self, year, cal_type, month_list):
        month_names = self.months[cal_type]  # Could include leap months not
        # in current year.
        months = []
        # print(cal_type, month_list)
        for m in month_list:
            months.append([m[0], month_names[m[1] - 1]])
        months.reverse()  # Print list from bottom up.

        # print('\startbuffer[%s]' % (cal_type + '_months'))
        output = (
            r"\\begin{tabular}{ |" + " ".join("m{1.3cm} |" for m in months) + "}" + "\n"
        )
        output += r"\hline" + "\n"
        output += " & ".join(m[1] for m in months) + r" \\" + "\n"
        output += r"\hline" + "\n"
        output += " & ".join(str(m[0]) for m in months) + r" \\" + "\n"
        output += r"\hline" + "\n"
        output += r"\end{tabular}" + "\n"
        return output

    def formatday(self, day, pos, index):
        """
        Returns a formatted day.
        """
        if day == 0:
            s = " "
        else:
            if day == 1 or day == r"{\moonphase a}":
                if pos == index and index != 6:
                    s = r"\multicolumn{{1}}{{|c}}{{{}}}".format(day)
                elif pos == index and index == 6:
                    s = r"\multicolumn{{1}}{{|c|}}{{{}}}".format(day)
                else:
                    s = "{} ".format(day)
            else:
                s = "{} ".format(day)
        return s

    def formatweek(self, theweek, new_moons=None):
        """
        Returns a single week in a string (no newline). Outlines the month by
        printing out horizontal rules along the top and bottom. The cells will
        get a vertical rule for the first day of the month.
        """
        print_iso_numbers = True
        indx = 0
        first_of_month = [i for (i, x) in enumerate(theweek[1]) if x == 1]
        week_details_dict, week_days_list = theweek
        if "new_moon" in week_details_dict:
            nm = week_details_dict["new_moon"][-1]
            for (i, dd) in enumerate(week_days_list):
                if dd == nm:
                    week_days_list[i] = r"{\moonphase a}"
            if "new_moon_fixed" in week_details_dict:
                i_new_moon = week_details_dict["new_moon_fixed"]
                t_new_moon = pcc.clock_from_moment(new_moons[i_new_moon][2])
                hour = int(t_new_moon[0])
                minute = int(t_new_moon[1])
                ts = "{:02d}:{:02d}".format(hour, minute)
                # ts = ':'.join(str(t) for t in clock_from_moment(new_moons[i][2])[0:2])
                ts = r"\rotatebox{{270}}{{\small {}}}".format(ts)
                ts = r"\multirow{{4}}{{4mm}}[6mm]{{{}}}".format(ts)
                if "molad" in week_details_dict:
                    n = week_days_list["raw"][6][0]
                    d = pcc.hebrew_from_fixed(n)
                    i_molad = pcc.molad(pcc.standard_month(d), pcc.standard_year(d))
                    d_molad = pcc.hebrew_from_fixed(i_molad)
                    d_molad = "{}-{}-{}".format(
                        pcc.standard_year(d_molad),
                        pcc.standard_month(d_molad),
                        int(pcc.standard_day(d_molad)),
                    )
                    # d_molad = '{:.3} {}'.format(DAYS_OF_WEEK_NAMES[d_molad],d_pretty)
                    # d_molad = '{}'.format(d_pretty)
                    t_molad = pcc.clock_from_moment(i_molad)
                    hour = int(t_molad[0])
                    minute = int(t_molad[1])
                    ts_molad = "{:02d}:{:02d}".format(hour, minute)
                    ts_molad = r"\rotatebox{{270}}{{\small {}}}".format(ts_molad)
                    ts_molad = r"\multirow{{4}}{{4mm}}[6mm]{{{}}}".format(ts_molad)
                    ts = r"\rotatebox{{270}}{{\small {}}}".format(d_molad)
                    ts = r"\multirow{{4}}{{4mm}}[6mm]{{{}}}".format(ts)
            else:
                ts = "test"
            theweek[1].append(ts)
            if "molad" in theweek[0]:
                theweek[1].append(ts_molad)
        if len(first_of_month) == 1:
            indx = first_of_month[0]
            top = r"\cline{{{}-8}}".format(indx + 1 + 1) + "\n"
            wf = "&".join(
                self.formatday(d, i, indx) for (i, d) in enumerate(theweek[1])
            )
            wf = str(week_details_dict["iso"]) + "&" + wf + r"\\" + "\n"
            if indx == 0:
                output = top + wf
            else:
                bottom = r"\cline{{2-{}}}".format(indx + 1) + "\n"
                output = top + wf + bottom
        else:  ## Regular week.
            wf = "&".join(self.formatday(d, i, -1) for (i, d) in enumerate(theweek[1]))
            wf = str(week_details_dict["iso"]) + "&" + wf + r"\\" + "\n"
            output = wf
        return output

    def format_iso_weeks(self, iso_list, year):
        # print '\startbuffer[isoweeks]'
        ##table_header = '\starttable[|c|]'
        table_header = r"\begin{tabular}{| c |}"
        output = table_header + r"\hline" + "\n"
        counter = 1
        for i in iso_list:
            if i[0] == year - 1:
                output += r" 52 \\" + "\n"
            elif i[0] == year + 1:
                output += r" 1 \\" + "\n"
            else:
                for j in range(0, i[2]):
                    output += r" %d \\" % counter + "\n"
                    counter += 1
            output += r"\hline" + "\n"
        output += r"\end{tabular}" + "\n"
        return output

    def prcandybar(self, year, cal_type, new_moons=None):
        month_list = []
        if cal_type == "gregorian":
            days = [d for d in self.iteryeardays3(year)]
            #             weeks = [days[i:i+7] for i in range(0, len(days), 7)]
            weeks, iso_list = self.isoweeks(year)
        # 	for w in weeks: print self.formatweek(w)
        else:
            data = [d for d in self.iteryeardays2_Hebrew(year, cal_type)]
            days = [d[0] for d in data]
            for d in data:
                if d[1] not in month_list:
                    month_list.append(d[1])
                self.formatmonthnames(year, cal_type, month_list)
                weeks = [days[i : i + 7] for i in range(0, len(days), 7)]
        output = r"\begin{tabular}{ccccccc}" + "\n"
        for w in weeks:
            output += self.formatweek(w, new_moons)
        output += r"\end{tabular}" + "\n"
        return output

    def prweeks(self, weeks, new_moons=None):

        candybar_template = Template(self.candybar_template_text)
        output = candybar_template.render(
            weeks=[self.formatweek(w, new_moons) for w in weeks]
        )
        return output


@click.command()
@click.option("--weeks-before", default=1, help="ISO week number.")
@click.option("--weeks_after", default=0)
@click.option("--year", default=2020, help="The calendar year.")
def main(year, weeks_before, weeks_after):
    cal = TextCandyBar(year, weeks_before=weeks_before, weeks_after=weeks_after)
    cal.prcandybar()


if __name__ == "__main__":
    main()
