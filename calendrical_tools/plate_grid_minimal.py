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
				stroke: lightgrey;
				stroke-width: 0.5;
			}
			#axis {
				fill: none;
				stroke: #859e6d;
				stroke-width: 0.5;				
			}
			#axis_plate {
				fill: none;
				stroke: lightgrey;
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
			#rect7 {
				fill: none !important;
			}
			#polygon9,
			#polygon11,
			#polygon13,
			#polygon15,
			#polygon17,
			#polygon19,
			#polygon21,
			#polygon23,
			#polygon25,
			#polygon27,
			#polygon29,
			#polygon31,
			#polygon33,
			#polygon35,
			#polygon37,
			#polygon39 {
				stroke: #859e6d !important;
				stroke-width: 0.5 !important;
				vector-effect: non-scaling-stroke;
				fill: #eafee7 !important;
			}
			#line43,
			#line45,
			#line47 {
				display: none;
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

	<g transform="translate(100, 100)" style="fill: #859e6d; font-size: 9px;">
		<title>Hawaiian Islands</title>
    	<g id="map" transform="translate(-15, 15), scale(0.05)">
    		{{ include_file('USA_Hawaii_location_map.svg') }}
    	</g>
		<text id="description" x="0" y="{{ -35 + RCapricorn - 19 }}" text-anchor="middle">
			{{ place_name }}
    		<tspan x="0" dy="1.2em">{{ latitude }} </tspan>
    	</text>
    </g>

	<g transform="translate(100, 100), scale(1, -1)">

		<g id="plate">
			<title>Astrolabe Plate</title>
			<g id="upperHorizon">
				<title>Horizon</title>
				<use xlink:href="#horizonPath" />
			</g>

			<g style="clip-path: url(#horizon);">
				<g id="azimuth">
					<title>Azimuth</title>
					{% for coord in azimuth_coords %}
						<circle cx="{{ coord.cx }}" cy="{{ coord.cy }}" 
						         r="{{ coord.r }}"/>
					{%- endfor %}		
				</g>
			</g>

			<g id="almucantar">
				<title>Almucantar</title>
				{% for coord in almucantar_coords %}
					<circle cx="{{ coord.cx }}" cy="{{ coord.cy }}" 
					        r="{{ coord.r }}"/>
				{%- endfor %}
			</g>

			<g id="axis_plate">
				<title>Axes</title>
				<line id="axis_plate" x1="0" y1="{{ RCapricorn }}" x2="0" y2="{{ -RCapricorn }}" />
				<line id="axis_plate" x1="{{ -RCapricorn }}" y1="0" x2="{{ RCapricorn }}" y2="0" />
			</g>
		</g>	

		<g id="tropics">
			<title>Tropic Circles</title>
			<g>
				<title>Tropic of Capricorn</title>
				<circle id="tropics" cx="0" cy="0" r="{{ RCapricorn }}"/>
			</g>
			<g>
				<title>Equator</title>
				<circle id="tropics" cx="0" cy="0" r="{{ REquator }}" />
			</g>
			<g>
				<title>Tropic of Cancer</title>
				<circle id="tropics" cx="0" cy="0" r="{{ RCancer }}" />
			</g>
		</g>

		<g id="axis">
			<title>Axes</title>
			<line id="axis" x1="0" y1="{{ RCapricorn }}" x2="0" y2="{{ -RCapricorn }}" />
			<line id="axis" x1="{{ -RCapricorn }}" y1="0" x2="{{ RCapricorn }}" y2="0" />
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

	with open('plate_template.svg', 'w') as fp:
		fp.write(plate_template)

	# template = jinja2.Template(plate_template)
	# svg = template.render(
	# 	RCapricorn=RadiusCapricorn,
	# 	REquator=RadiusEquator,
	# 	RCancer=RadiusCancer,
	# 	place_name=place,
	# 	latitude=latitude,
	# 	horiz=horiz,
	# 	azimuth_coords=azimuth_coords,
	# 	almucantar_coords=almucantar_coords
	# )

	import jinja2

	# Seems like overkill, but adds "include_file" function to jinja2
	# environment in order to include raw svg into an html template.
	@jinja2.contextfunction                                                                                                                                                                                         
	def include_file(ctx, name):                                                                                                                                                                                   
	    env = ctx.environment                                                                                                                                                                                      
	    return jinja2.Markup(env.loader.get_source(env, name)[0])


	loader = jinja2.PackageLoader(__name__, '.')                                                                                                                                                       
	env = jinja2.Environment(loader=loader)                                                                                                                                                                    
	env.globals['include_file'] = include_file                                                                                                                                                                 

	svg = env.get_template('plate_template.svg').render(
		RCapricorn=RadiusCapricorn,
		REquator=RadiusEquator,
		RCancer=RadiusCancer,
		place_name=place,
		latitude=latitude,
		horiz=horiz,
		azimuth_coords=azimuth_coords,
		almucantar_coords=almucantar_coords
	) 

	with open('plate.svg', 'w') as fp:
		fp.write(svg)

if __name__ == "__main__":
    main()
