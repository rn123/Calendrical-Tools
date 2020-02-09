# OSX iterm2 environment with TeXLive and iterm2 integration.
astrolabe:
	cd calendrical_tools; python generate_astrolabe.py; cd ..
	mv calendrical_tools/astrolabe_generated.svg docs/assets/images
	mv calendrical_tools/astrolabe_generated.html docs/

plate:
	cd calendrical_tools; python plate_grid_minimal.py; cd ..
	mv calendrical_tools/plate.svg docs/_includes
	cp docs/_includes/plate.svg docs/assets/images/

tex:
	python display_candybars.py

output/cal_2020.tex:
	python display_candybars.py

cal.png: output/cal_2020.tex
	cd output;lualatex cal_2020.tex; cd ..
	gs -q -dNOPAUSE -dBATCH -sDEVICE=pngalpha -sOutputFile=output/cal_2020.png -r600 output/cal_2020.pdf

view: cal.png
	imgcat output/cal_2020.png

clean:
	rm output/*
