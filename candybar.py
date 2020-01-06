#!/usr/bin/env python
# coding: utf-8

import datetime
import json
import pycalcal as pcc 

class CandyBar():
    firstweekday = 0
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
                twoweeks=datetime.timedelta(days=14)
            while True:
                yield date
                date += twoweeks
            if date.month != month:
                break

    def isoweeks(self, g_year):
        """
        ISO weeks determined by nth Thursdays.
        """
        ## Use pycalcal to find first Thursday of the year. Returns an integer 
        ## day count of days elapsed since 1/1/1 (rata die -- fixed day).
        first_thursday = pcc.nth_kday(1, 4, [g_year, 1, 1])
        ## Back up and enumerate days starting the week before.
        days = [first_thursday - 3 - 7 + j for j in range(0,54*7)]
        days_dates = [(d, pcc.gregorian_from_fixed(d)) for d in days]
        ## List of weeks, starting on Mondays  
        weeks = [days_dates[i:i+7] for i in range(0, len(days_dates), 7)]

        ## Count weeks (actually starting Mondays) in each month.
        iso = dict()
        iso_list = []
        for w in weeks:
            # Key is the year and month of the starting Monday.
            key = str(pcc.standard_year(w[0][1])) + '_' + str(pcc.standard_month(w[0][1]))
            if key not in iso.keys():
                iso[key] = 1
            else:
                iso[key] += 1
        ## A dictionary was used to accumulate count. Now create sorted list of 
        ## months with count of how many iso weeks (Mondays) start in that month.
        for k in iso.keys():
            pair = list(map(int, k.split('_')))
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

    def iterHebrewYearDates(self, g_year):
        """
        Return an iterator for one year. The iterator will yield Hebrew dates
        corresponding to the gregorian year and will always iterate
        through complete weeks, so it will yield dates outside the specified year.
        """
        date = datetime.date(g_year, 1, 1)
        # Go back to the beginning of the week
        days = (date.weekday() - self.firstweekday) % 7
        date -= datetime.timedelta(days=days)
        oneday = datetime.timedelta(days=1)
        while True:
            yield pcc.hebrew_from_fixed(pcc.fixed_from_gregorian([date.year, date.month, date.day]))
            date += oneday
            if date.year != g_year and date.weekday() == self.firstweekday:
                break

    def iteryeardays2_Hebrew(self, g_year, cal_type):
        """
        Like iteryeardates(), but will yield (day number, weekday number)
        tuples. For days outside the specified month the day number is 0.
        """
        for date in self.iteryeardates(g_year):
            if date.year != g_year:
                fd = pcc.fixed_from_gregorian([date.year, date.month, date.day])
                d = pcc.hebrew_from_fixed(fd)
                day_value = pcc.standard_day(d)
                month_value = pcc.standard_month(d)
                year_value = pcc.standard_year(d)
                yield [(0, date.weekday()),(year_value, month_value)]
            else:
                fd = pcc.fixed_from_gregorian([date.year, date.month, date.day])
                if cal_type == 'hebrew':
                    d = pcc.hebrew_from_fixed(fd)
                    day_value = pcc.standard_day(d)
                    month_value = pcc.standard_month(d)
                    year_value = pcc.standard_year(d)
                elif cal_type == 'chinese':
                    d = pcc.chinese_from_fixed(fd)
                    day_value = pcc.chinese_day(d)
                    month_value = pcc.chinese_month(d)
                else:
                    print('type %s not implemented' % cal_type)
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

    def candybar(self, year):
        days = [d for d in self.iteryeardays3(year)]
        return [days[i:i+7] for i in range(0, len(days), 7)]

class TextCandyBar(CandyBar):
    def formatday(self, day, weekday, width):
        """
        Returns a formatted day.
        """
        if day == 0:
            s = ''
        else:
            s = '%02i' % day             # right-align single-digit days
        return s.center(width)
    
    def formatweek(self, week):
        formatted_week = ' '.join(['{:2}'.format(d[2]) for m,d in week])
        formatted_week = formatted_week.replace(' 0', '  ')
        return formatted_week

    def prcandybar(self, year):
        weeks, iso_list = self.isoweeks(year)
        iso_week_numbers = [pcc.iso_week(pcc.iso_from_fixed(w[0][0])) for w in weeks]
        for iw, w in zip(iso_week_numbers, weeks):
            print('{:2}'.format(iw) + '\t' + self.formatweek(w))

    def prhebrewcandybar(self, year):
        days = [d for d in self.iteryeardays2_Hebrew(year)]
        weeks = [days[i:i+7] for i in range(0, len(days), 7)]
        for w in weeks:
            print(self.formatweek(w))

class LaTeXCandyBar(CandyBar):
    months = {'gregorian':['January', 'February', 'March', 'April',
    'May', 'June','July', 'August', 'September',
    'October', 'November', 'December'],
    'hebrew':['Nisan', 'Iyyar', 'Sivan', 'Tammuz', 'Av',
    'Elul','Tishri','Marheshvan', 'Kislev', 'Tevet',
    'Shevat', 'Adar', 'Adar II']}

    def formatmonthnames(self, year, cal_type, month_list):
        month_names = self.months[cal_type] # Could include leap months not
                                                                        # in current year.
        months = []
        #print(cal_type, month_list)
        for m in month_list: months.append([m[0],month_names[m[1]-1]])
        months.reverse() # Print list from bottom up.

        #print('\startbuffer[%s]' % (cal_type + '_months'))
        output = r'\\begin{tabular}{ |' + ' '.join('m{1.3cm} |' for m in months)+'}' + '\n'
        output += r'\hline' + '\n'
        output += ' & '.join(m[1] for m in months) + r' \\' + '\n'
        output += r'\hline' + '\n'
        output += ' & '.join(str(m[0]) for m in months) + r' \\' + '\n'
        output += r'\hline' + '\n'
        output += r'\end{tabular}' + '\n'
        return output

    def formatday(self, day, pos, index):
        """
        Returns a formatted day.
        """
        if day == 0:
            s = ' '
        else:
            if day == 1 or day == r'\newmoon':
                if pos == index and index != 6:
                    s = r'\multicolumn{{1}}{{|c}}{{{}}}'.format(day)
                elif  pos == index and index == 6:
                    s = r'\multicolumn{{1}}{{|c|}}{{{}}}'.format(day)
                else:
                    s = '{} '.format(day)
            else:
                    s = '{} '.format(day)
        return s

    def formatweek(self, theweek, new_moons=None):
        """
        Returns a single week in a string (no newline). Outlines the month by
        printing out horizontal rules along the top and bottom. The cells will
        get a vertical rule for the first day of the month.
        """
        print_iso_numbers = True 
        indx = 0
#         print(theweek)
        first_of_month = [i for (i,x) in enumerate(theweek[1]) if x == 1]
        if 'new_moon' in theweek[0].keys(): 
            nm = theweek[0]['new_moon'][-1]
            for (i,dd) in enumerate(theweek[1]):
                if dd == nm: theweek[1][i] = r'\newmoon'
            #print first_of_month, theweek
            if 'new_moon_fixed' in theweek[0].keys():
                i_new_moon = theweek[0]['new_moon_fixed']
                t_new_moon = pcc.clock_from_moment(new_moons[i_new_moon][2])
                hour = int(t_new_moon[0])
                minute = int(t_new_moon[1])
                #print type(hour), type(minute)
                ts = '{:02d}:{:02d}'.format(hour,minute)
                #ts = ':'.join(str(t) for t in clock_from_moment(new_moons[i][2])[0:2])
                ts = r'\rotatebox{{270}}{{\small {}}}'.format(ts)
                ts = r'\multirow{{4}}{{4mm}}[6mm]{{{}}}'.format(ts)
                if 'molad' in theweek[0].keys():
                    #print theweek
                    n = theweek[0]['raw'][6][0]
                    d = pcc.hebrew_from_fixed(n)
                    #print n,d
                    #print standard_year(d),standard_month(d)
                    i_molad = pcc.molad(pcc.standard_month(d), pcc.standard_year(d))
                    d_molad = pcc.hebrew_from_fixed(i_molad)
                    #print i_molad,d_molad
                    d_molad = '{}-{}-{}'.format(pcc.standard_year(d_molad),
                            pcc.standard_month(d_molad), int(pcc.standard_day(d_molad)))
                    #d_molad = '{:.3} {}'.format(DAYS_OF_WEEK_NAMES[d_molad],d_pretty)
                    #d_molad = '{}'.format(d_pretty)
                    t_molad = pcc.clock_from_moment(i_molad)
                    hour = int(t_molad[0])
                    minute = int(t_molad[1])
                    #print hour, minute,t_molad
                    ts_molad = '{:02d}:{:02d}'.format(hour, minute)
                    ts_molad = r'\rotatebox{{270}}{{\small {}}}'.format(ts_molad)
                    ts_molad = r'\multirow{{4}}{{4mm}}[6mm]{{{}}}'.format(ts_molad)
                    ts = r'\rotatebox{{270}}{{\small {}}}'.format(d_molad)
                    ts = r'\multirow{{4}}{{4mm}}[6mm]{{{}}}'.format(ts)
            else: 
                ts = 'test'
            #print theweek[1]
            theweek[1].append(ts)
            if 'molad' in theweek[0].keys():
                theweek[1].append(ts_molad)
            #print theweek[1]
            #print  r'{}'.format(ts)+ r'\\'
        if len(first_of_month) == 1:
            indx = first_of_month[0]
            #print 'indx = ', indx
            top = r'\cline{{{}-8}}'.format(indx+1+1) + '\n'
            wf = '&'.join(self.formatday(d, i, indx) for (i,d) in enumerate(theweek[1]))+ r'\\' + '\n'
            wf = str(theweek[0]['iso']) + '&' + wf
            if indx == 0:
                output = top + wf
            else: 
                bottom = r'\cline{{2-{}}}'.format(indx+1) + '\n'
                output = top + wf + bottom
        else:           ## Regular week.
            wf = '&'.join(self.formatday(d, i, -1) for (i,d) in enumerate(theweek[1])) + r'\\' + '\n'
            wf = str(theweek[0]['iso']) + '&' + wf
            output = wf
        return output

    def format_iso_weeks(self, iso_list, year):
        #print '\startbuffer[isoweeks]'
        ##table_header = '\starttable[|c|]'
        table_header = r'\begin{tabular}{| c |}'
        output =  table_header + r'\hline' + '\n'
        counter = 1
        for i in iso_list:
            if i[0] == year - 1:
                output += r' 52 \\' + '\n'
            elif i[0] == year +1:
                output += r' 1 \\' + '\n'
            else:
                for j in range(0,i[2]):
                    output += r' %d \\' % counter + '\n'
                    counter += 1
            output += r'\hline' + '\n'
        output += r'\end{tabular}' + '\n'
        return output

    def prcandybar(self, year, cal_type, new_moons=None):
        month_list = []
        if cal_type == "gregorian":
            days = [d for d in self.iteryeardays3(year)]
#             weeks = [days[i:i+7] for i in range(0, len(days), 7)]
            weeks, iso_list = self.isoweeks(year)
        #	for w in weeks: print self.formatweek(w)
        else:
            data = [d for d in self.iteryeardays2_Hebrew(year, cal_type)]
            days = [d[0] for d in data]
            for d in data:
                if d[1] not in month_list:
                    month_list.append(d[1])
                self.formatmonthnames(year, cal_type, month_list)
                weeks = [days[i:i+7] for i in range(0, len(days), 7)]
        output = r'\begin{tabular}{ccccccc}' + '\n'
        for w in weeks: 
            output += self.formatweek(w, new_moons)
        output += r'\end{tabular}' + '\n'
        return output

    def prweeks(self, weeks, new_moons=None):
        month_list = []

        output = r'\begin{tabular}{l|ccccccc|rr}' + '\n'
        for w in weeks: 
            output += self.formatweek(w, new_moons)
        output += r'\end{tabular}' + '\n'
        return output
