import math
import jinja2

obliquity=23.4443291
RadiusCapricorn = 100
obliquityRadiansArgument = math.radians((90 - obliquity) / 2)
RadiusEquator = RadiusCapricorn * math.tan( obliquityRadiansArgument )
RadiusCancer = RadiusEquator * math.tan( obliquityRadiansArgument )

plate_template = '''
<svg viewbox="0 0 210 210" 
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
	<defs>
		<style type="text/css">
			#plate {
				fill: none;
				stroke: #859e6d;
				stroke-width: 0.5;
				clip-path: url(#horizon);
			}
			#tropics {
				fill: none;
				stroke: #859e6d;
				stroke-width: 0.5;
			}
			#vert {
				fill: none;
				stroke: #859e6d;
				stroke-width: 0.5;				
			}
			#upperHorizon {
				stroke: #859e6d;
				stroke-width: 1;
				fill: #eafee7;
				clip-path: url(#capricorn);
			}
			#capricornPath {
				stroke: #859e6d;
				stroke-width: 0.5;
				fill: none;
			}
			#azimuth {
				fill: none;
				stroke: #859e6d;
				stroke-width: 0.5;
				clip-path: url(#horizon);
				clip-path: url(#capricorn);
			}
			#almucantar {
				fill: none;
				stroke: #859e6d;
				stroke-width: 0.5;
				clip-path: url(#capricorn);
			}
		</style>

		<clipPath id="capricorn">
			<path id="capricornPath" d="
					M0 {{ RCapricorn }}
					A{{ RCapricorn }} {{ RCapricorn }} 0 0 1 0 {{ -RCapricorn }}
					A{{ RCapricorn }} {{ RCapricorn }} 0 0 1 0 {{ RCapricorn }}z"/>
		</clipPath>

		<clipPath id="horizon">
			<path id="horizonPath" d="
					M{{ horiz.cx }} {{ horiz.cy + horiz.r }} 
					A{{ horiz.r }} {{ horiz.r }} 0 0 1 {{ horiz.cx }} {{ horiz.cy - horiz.r }}
					A{{ horiz.r }} {{ horiz.r }} 0 0 1 {{ horiz.cx }} {{ horiz.cy + horiz.r }}z
				"/>
		</clipPath>
	</defs>
	
	
	<g id="plate" transform="translate(100, 100), scale(1, -1)">

		<g id="upperHorizon">
			<use xlink:href="#horizonPath" />
		</g>

		<g style="clip-path: url(#horizon);">
			<g id="azimuth">
				{% for coord in azimuth_coords %}
					<circle cx="{{ coord.cx }}" cy="{{ coord.cy }}" 
					         r="{{ coord.r }}"/>
				{%- endfor %}		
			</g>
		</g>

		<g id="almucantar">
			{% for coord in almucantar_coords %}
				<circle cx="{{ coord.cx }}" cy="{{ coord.cy }}" 
				        r="{{ coord.r }}"/>
			{%- endfor %}
		</g>

		<g id="tropics">
			<circle id="tropics" cx="0" cy="0" r="{{ RCapricorn }}"/>
			<circle id="tropics" cx="0" cy="0" r="{{ REquator }}" style="display:none"/>
			<circle id="tropics" cx="0" cy="0" r="{{ RCancer }}" style="display:none"/>
			<line id="vert" x1="0" y1="{{ RCapricorn }}" x2="0" y2="{{ -RCapricorn }}" />
		</g>
	</g>
</svg>
'''


def almucantar_arc(altitude=None, latitude=None):
        radiansAltitude = math.radians(altitude)
        radiansLatitude = math.radians(latitude)

        almucantorCenter = RadiusEquator * (
            math.cos(radiansLatitude)
            / (math.sin(radiansLatitude) + math.sin(radiansAltitude))
        )

        almucantarRadius = RadiusEquator * (
            math.cos(radiansAltitude)
            / (math.sin(radiansLatitude) + math.sin(radiansAltitude))
        )
        return {
        	"alt": altitude, 
      		"cx": 0, 
           	"cy": almucantorCenter, 
           	"r": almucantarRadius
     	}


def azimuth_arc(azimuth=None, latitude=None):
    radiansMinus = math.radians((90 - latitude) / 2.0)
    radiansPlus = math.radians((90 + latitude) / 2.0)

    yZenith = RadiusEquator * math.tan(radiansMinus)
    yNadir = -RadiusEquator * math.tan(radiansPlus)
    yCenter = (yZenith + yNadir) / 2.0
    yAzimuth = (yZenith - yNadir) / 2.0

    radiansAzimuth = math.radians(azimuth)
    xAzimuth = yAzimuth * math.tan(radiansAzimuth)
    radiusAzimuth = yAzimuth / math.cos(radiansAzimuth)

    coord_left = {
        "az": azimuth,
        "cx": xAzimuth,
        "cy": yCenter,
        "r": radiusAzimuth,
    }
    coord_right = {
        "az": azimuth,
        "cx": -xAzimuth,
        "cy": yCenter,
        "r": radiusAzimuth,
    }
    return [coord_left, coord_right]


def horizon(latitude=None):
        radiansLatitude = math.radians(latitude)
        rHorizon = RadiusEquator / math.sin(radiansLatitude)
        yHorizon = RadiusEquator / math.tan(radiansLatitude)
        xHorizon = 0.0
        return {"cx": xHorizon, "cy": yHorizon, "r": rHorizon}


def main():
	place, latitude = ("Hawaiian Islands", 21.3069)

	azimuth_coords = []
	for azimuth in list(range(0, 90, 10)):
		coords = azimuth_arc(azimuth=azimuth, latitude=latitude)
		azimuth_coords.extend(coords)

	almucantar_coords = []
	for altitude in list(range(10, 90, 10)):
		coords = almucantar_arc(altitude=altitude, latitude=latitude)
		almucantar_coords.append(coords)

	horiz = horizon(latitude)
	print(place, latitude)

	template = jinja2.Template(plate_template)
	svg = template.render(
    	RCapricorn=RadiusCapricorn,
    	REquator=RadiusEquator,
    	RCancer=RadiusCancer,
    	horiz=horiz,
    	azimuth_coords=azimuth_coords,
    	almucantar_coords=almucantar_coords
    )

	with open('plate.svg', 'w') as fp:
		fp.write(svg)

if __name__ == "__main__":
    main()
