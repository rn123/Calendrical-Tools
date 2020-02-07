<img src="{{ "/assets/images/card_lunar_new_year_rat.svg" | relative_url }}" alt="idea card" width="100%" style="padding:5px;"/>

Organizing and visualizing the counts of days, moons, and years is fundamental. Over the centuries, many devices have been invented for this purpose, resulting in the rich calendrical and astronomical traditions of world history. Calendrical-Tools builds calendars, diagrams, and timelines to help explore these traditions and their first principles as well as to produce useful devices for managing time from a historically accurate point of view.

Inspired by David Seah's [Compact Calendar](https://davidseah.com/node/compact-calendar/) project that produces a one-page time-management tool, ```candybar.py``` is a set of code that computes "candybar calendars" for various calendrical traditions. The candybar view of time organizes day counts into ISO weeks and stacks the weeks up to fill in a calendar year. David Seah introduced the idea of calling these candybar calendars: 
<img src="{{ "/assets/images/compact_calendar.png" | relative_url }}" alt="Compact Calendar" width="30%" align="right" style="padding:5px;"/>

> The Compact Calendar presents days as a continuous candy bar of time. Because the weeks are presented as a stack of available time, it’s easy to block out days naturally as you think. There’s a lot of free space available on the right-side of the sheet for note taking.

Amature astronomy and computational inspirations are from the fantasic books by Reingold & Dershowitz, "Calendrical Computations" and James Morrison, "The Astrolabe." 

Close study of Reingold & Dershowitz (mainly from the 3rd edition, although my copy of the 4th edition is on it's way from Amazon) and the [python implementation](https://github.com/espinielli/pycalcal) by Enrico Spinielli, as well as cited references, has been a factor in my amature astronomy passion for a long time.

<img src="{{ "/assets/images/pocket_sundial.png" | relative_url }}" alt="THE KALA POCKET SUNDIAL" width="25%" align="right" style="padding:5px;"/>
Likewise, the study of computing and drawing astrolabes inspired by James Morrison, has been a passion. In the 90's I bought his laminated cardboard astrolabes (and later his book) that have fed a passion for decades. By the way, if working versions of ancient astrolabes is your thing, you should also take a look at [Kala's pocket sundial](https://www.pocket-sundial.com/products/kala-sundial).

The concept of the project is to develop tools on top of Spinielli's pycalcal. Pycalcal is a python version of Reingold & Dershowitz's lisp implementation (calendrica 3.0) software.  Based on Reingold & Dershowitz, the Calendrical-Tools can compute candybar calendars that are accurate over the historical period and in the many calendrical traditions. The visualizations of the sky borrowed from the geometric construction of astrolabes adds to the tabular forms of calendars.

The [beautiful reconstructions of historical mathematical tables](https://locomat.loria.fr/locomat/reconstructed.html) by [Denis Roegel](https://members.loria.fr/Roegel/highlights.html) has been a major influence on producing quality latex output. There is also a wide variety of old tables (and calendars) that would be interesting to reproduce.
<img src="{{ "/assets/images/screenshot.png" | relative_url }}" alt="command line screenshot of candybar.py" width="100%" style="padding:5px;"/>
