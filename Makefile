# OSX iterm2 environment with TeXLive and iterm2 integration.

tex:
	python display_candybars.py

output/cal_2020.tex:
	python display_candybars.py

cal.png: output/cal_2020.tex
	cd output;latex cal_2020.tex;dvipdf cal_2020.dvi; cd ..
	gs -q -dNOPAUSE -dBATCH -sDEVICE=pngalpha -sOutputFile=cal.png -r144 output/cal_2020.pdf

view: cal.png
	imgcat cal.png

clean:
	rm output/*