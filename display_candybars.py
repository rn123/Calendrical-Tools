#!/usr/bin/env python
# coding: utf-8

import datetime
import json
from calendar import TextCalendar, Calendar, HTMLCalendar
from candybar import *  

cal = TextCalendar()
print(cal.formatyear(2020))

cal = TextCandyBar()
cal.prcandybar(2020)

year = 2020
cal = LaTeXCandyBar()
new_moons_data = [(n, nth_new_moon(n)) for n in range(24970,24985)]
new_moons = {}
for record in new_moons_data:
    n = record[0] 
    nnm = nth_new_moon(n)
    nm = gregorian_from_fixed(nnm)
    key = int(nnm)
    new_moons[key] = (n, nm, nnm)

wks, iso = cal.isoweeks(year)
#print wks
weeks = []
for w in wks:
    iso_week_number = iso_week(iso_from_fixed(w[0][0]))
    week_data = {}
    week_data['iso'] = iso_week_number
    week_data['raw'] = w
    for d in w:
        if d[0] in new_moons.keys():
            week_data['new_moon'] = gregorian_from_fixed(d[0])
            week_data['new_moon_fixed'] = d[0]
#             print(week_data)
    week = [week_data]
    week.append([standard_day(gregorian_from_fixed(d[0])) for d in w])
    weeks.append(week)
# print(cal.prweeks(weeks))
# print('&')
# print(r"""
# \begin{tabular}{c}
# """)
# for w in weeks:
#     if 'new_moon' in w[0].keys():
#         i = w[0]['new_moon_fixed']
#         #print str(new_moons[i][2]) + r'\\'
#         ts = ':'.join(str(t) for t in clock_from_moment(new_moons[i][2])[0:2])
#         print(r'{}'.format(ts)+ r'\\')
#     else: 
#         print(r'\\')
# print(r"""
# \end{tabular}
# &
# """)

year = 2020
hstart = standard_year(hebrew_from_fixed(fixed_from_gregorian([year,1,1])))
hend = standard_year(hebrew_from_fixed(fixed_from_gregorian([year,12,1])))
istart = standard_year(islamic_from_fixed(fixed_from_gregorian([year,1,1])))
iend = standard_year(islamic_from_fixed(fixed_from_gregorian([year,12,1])))

cal = LaTeXCandyBar()

output = r"""
\documentclass[9pt,landscape]{article}
\usepackage{calc,layouts,graphicx,wasysym,multirow,array}
\usepackage[lmargin=40pt,tmargin=40pt,bmargin=0pt]{geometry}
\pagestyle{empty}
\begin{document}

\resizebox{!}{9cm}{

\begin{tabular}{|c|c|c|c|c|}
\hline
Gregorian & Lunar & Hebrew & Islamic & Chinese \\
"""

output += r'{}& Phases & {}/{}& {}/{}& \\'.format(year,hstart,hend,istart,iend) + '\n'
output += r'\hline' + '\n'

for y in range(year, year+29):
    wks, iso = cal.isoweeks(y)
    first_thursday = nth_kday(1, 4, [y, 1, 1])
    t1 = gregorian_from_fixed(first_thursday)
    monday = gregorian_from_fixed(first_thursday - 3)
#     print(monday, t1, is_iso_long_year(y))
#     print(iso_from_fixed(fixed_from_gregorian([y,1,1])))
#     print(wks[0])
#     print(wks[-1])

# cal.prcandybar(year,"gregorian")
#cal.prcandybar(year,"hebrew")
#cal.prcandybar(year,"chinese")

first_thursday = nth_kday(1, 4, [year, 1, 1])
wks, iso = cal.isoweeks(year)
# print(cal.format_iso_weeks(iso, year))

new_moons_data = [(n, nth_new_moon(n)) for n in range(24970,24985)]
new_moons = {}
for record in new_moons_data:
    n = record[0] 
    nnm = nth_new_moon(n)
    nm = gregorian_from_fixed(nnm)
    key = int(nnm)
    new_moons[key] = (n, nm, nnm)

wks, iso = cal.isoweeks(year)
# print(wks)
for cal_type in ["gregorian", "hebrew","islamic", "chinese"]:
    if cal_type == "gregorian":
        weeks = []
        for w in wks:
            iso_week_number = iso_week(iso_from_fixed(w[0][0]))
            week_data = {}
            week_data['iso'] = iso_week_number
            week_data['raw'] = w
            for d in w:
                if d[0] in new_moons.keys():
                    week_data['new_moon'] = gregorian_from_fixed(d[0])
                    week_data['new_moon_fixed'] = d[0]
#             print(week_data)
            week = [week_data]
            week.append([standard_day(gregorian_from_fixed(d[0])) for d in w])
            weeks.append(week)
        output += cal.prweeks(weeks, new_moons) + '\n'
        output += '&' + '\n'
        output += r"""
\begin{tabular}{c}
"""
        for w in weeks:
            if 'new_moon' in w[0].keys():
                i = w[0]['new_moon_fixed']
                #print str(new_moons[i][2]) + r'\\'
                ts = ':'.join(str(t) for t in clock_from_moment(new_moons[i][2])[0:2])
                output += r'{}'.format(ts)+ r'\\' + '\n'
            else: 
                output += r'\\' + '\n'
        output += r"""
\end{tabular}
&
"""
    elif cal_type == "hebrew":
        weeks = []
        for w in wks:
            iso_week_number = iso_week(iso_from_fixed(w[0][0]))
            week_data = {}
            week_data['iso'] = iso_week_number
            week_data['raw'] = w
            for d in w:
                if d[0] in new_moons:
                    hd = hebrew_from_fixed(d[0])
                    #print hd, d[0], w
                    week_data['new_moon'] = hd
                    week_data['molad'] = 'empty'
                    week_data['new_moon_fixed'] = d[0]
            #print week_data
            week = [week_data]
            week.append([standard_day(hebrew_from_fixed(d[0])) for d in w])
            weeks.append(week)
        output += cal.prweeks(weeks, new_moons) + '\n'
        output += '&\n' 
    elif cal_type == "islamic":
        weeks = []
        for w in wks:
            iso_week_number = iso_week(iso_from_fixed(w[0][0]))
            week_data = {}
            week_data['iso'] = iso_week_number
            week_data['raw'] = w
            for d in w:
                if d[0] in new_moons:
                    week_data['new_moon'] = islamic_from_fixed(d[0])
                    week_data['new_moon_fixed'] = d[0]
#                 print(week_data)
            week = [week_data]
            week.append([standard_day(islamic_from_fixed(d[0])) for d in w])
            weeks.append(week)
        output += cal.prweeks(weeks, new_moons) + '\n'
        output += '&\n'
    elif cal_type == "chinese":
        weeks = []
        if True:
            file_name = 'chinese_lunar_' + str(year)
            with open(file_name,'r') as f:
                weeks = json.load(f)
        else: 
            for w in wks:
                iso_week_number = iso_week(iso_from_fixed(w[0][0]))
                week = [iso_week_number]
                week_data = {}
                week_data['iso'] = iso_week_number
                week_data['raw'] = w
                for d in w:
                    if d[0] in new_moons:
                        week_data['new_moon'] = chinese_from_fixed(d[0])
                        week_data['new_moon_fixed'] = d[0]
#                 print(week_data)
                week = [week_data]
                week.append([chinese_day(chinese_from_fixed(d[0])) for d in w])
                weeks.append(week)
                file_name = 'chinese_lunar_' + str(year)
        with open(file_name, 'w') as f:
            json.dump(weeks,f)
        output += cal.prweeks(weeks, new_moons) + '\n'
        output += r'\\' + '\n'

# month_list = [(year,m) for m in range(1,13)]
# cal.formatmonthnames(year, 'gregorian', month_list)
# f = open('chinese_lunar_2020','w')
# json.dump(weeks,f)
# f.close()

# cal.prcalendars(year)
output += r"""
\hline
\end{tabular}}
\end{document}
 """

with open('cal_2020.tex', 'w') as fp:
    fp.write(output)
