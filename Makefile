# OSX iterm2 environment with TeXLive and iterm2 integration.

cal.png:
	python display_candybars.py
	cd output;latex cal_2020.tex;dvipdf cal_2020.dvi; cd ..
	gs -q -dNOPAUSE -dBATCH -sDEVICE=pngalpha -sOutputFile=cal.png -r144 output/cal_2020.pdf

view: cal.png
	imgcat cal.png