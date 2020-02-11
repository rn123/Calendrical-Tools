import math
import jinja2

from calendrical_tools.generate_astrolabe import *

obliquity = 23.4443291
RadiusCapricorn = 100
obliquityRadiansArgument = math.radians((90 - obliquity) / 2)
RadiusEquator = RadiusCapricorn * math.tan(obliquityRadiansArgument)
RadiusCancer = RadiusEquator * math.tan(obliquityRadiansArgument)


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
    return {"alt": altitude, "cx": 0, "cy": almucantorCenter, "r": almucantarRadius}


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
    plate_parameters = {"Hawaiian Islands": 21.3069}
    astrolabe = Astrolabe(plate_parameters=plate_parameters)
    plate = astrolabe.plates["Hawaiian Islands"]

    azimuth_coords = []
    for azimuth in list(range(0, 90, 10)):
        coords = azimuth_arc(azimuth=azimuth, latitude=latitude)
        azimuth_coords.extend(coords)

    almucantar_coords = []
    for altitude in list(range(10, 90, 10)):
        coords = almucantar_arc(altitude=altitude, latitude=latitude)
        almucantar_coords.append(coords)

    horiz = horizon(latitude)

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

    ecliptic = {
        "cx": astrolabe.xEclipticCenter,
        "cy": astrolabe.yEclipticCenter,
        "r": astrolabe.RadiusEcliptic,
        "width": 5,
    }

    outer_radius = ecliptic["r"]
    inner_radius = outer_radius - ecliptic["width"]

    top_middle_outer = {"x": (ecliptic["cx"]), "y": (ecliptic["cy"] + outer_radius)}
    bottom_middle_outer = {"x": (ecliptic["cx"]), "y": (ecliptic["cy"] - outer_radius)}

    top_middle_inner = {"x": (ecliptic["cx"]), "y": (ecliptic["cy"] + inner_radius)}
    bottom_middle_inner = {"x": (ecliptic["cx"]), "y": (ecliptic["cy"] - inner_radius)}

    aries_first_point = astrolabe.ecliptic_division(180)
    aries_first_point_angle = math.degrees(
        math.atan2(aries_first_point["y2"], aries_first_point["x2"])
    )

    ecliptic_divisions = []
    for angle in list(range(0, 361, 30)):
        ecliptic_divisions.append(astrolabe.ecliptic_division(angle))

    ecliptic_divisions_fine = []
    for angle in list(range(0, 361, 10)):
        ecliptic_divisions_fine.append(astrolabe.ecliptic_division(angle))

    ecliptic_divisions_efine = []
    for angle in list(range(0, 361, 2)):
        ecliptic_divisions_efine.append(astrolabe.ecliptic_division(angle))

    seasonal_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    seasonal_names = [
        "pisces",
        "aquarius",
        "capricorn",
        "sagittarius",
        "scorpio",
        "libra",
        "virgo",
        "leo",
        "cancer",
        "gemini",
        "taurus",
        "aries",
    ]

    angle = 0
    seasonal_arcs = []
    for n, division in enumerate(ecliptic_divisions[0:12]):
        tag = "season" + str(angle)
        angle += 30
        next_division = ecliptic_divisions[(n + 1) % 12]
        sarc = Path(
            Arc(
                start=complex(division["x2"], division["y2"]),
                radius=complex(ecliptic["r"], ecliptic["r"]),
                rotation=0.0,
                large_arc=True,
                sweep=False,
                end=complex(next_division["x2"], next_division["y2"]),
            )
        )
        seasonal_arcs.append(
            {
                "tag": tag,
                "name": seasonal_names[n],
                "r": ecliptic["r"],
                "start_x": division["x2"],
                "start_y": division["y2"],
                "end_x": next_division["x2"],
                "end_y": next_division["y2"],
                "reversed": sarc.reversed().d(),
            }
        )

    stars = [
        {"name":"aldebaran",  "r": 0.7467, "theta": 68.98},
        {"name":"altair",     "r": 0.8561, "theta": 297.69542},
        {"name":"arcturus",   "r": 0.7109, "theta": 213.91500},
        {"name":"capella",    "r": 0.4040, "theta": 79.17208},
        {"name":"sirius",     "r": 1.3099, "theta": 101.28708},
        {"name":"procyon",    "r": 0.9127, "theta":114.82542},
        {"name":"deneb",      "r": 0.4114, "theta": 310.35750},
        {"name":"castor",     "r": 0.5556, "theta": 113.64958},
        {"name":"regulus",    "r": 0.8103, "theta": 152.09250},
        {"name":"vega",       "r": 0.4793, "theta": 279.23417},
        {"name":"betelgeuse", "r": 0.8784, "theta": 88.79292},
        {"name":"rigel",      "r": 1.1463, "theta": 78.63417},
        {"name":"bellatrix",  "r": 0.8949, "theta": 81.28250},
        {"name":"antares",    "r": 1.5870, "theta": 247.35167},
        {"name":"spica",      "r": 1.2096, "theta": 201.29792}
    ]

    for star in stars:
        star["cx"] = astrolabe.RadiusEquator * star["r"] * math.cos(math.radians(star["theta"]))
        star["cy"] = astrolabe.RadiusEquator * star["r"] * math.sin(math.radians(star["theta"]))

    import jinja2

    # Seems like overkill, but adds "include_file" function to jinja2
    # environment in order to include raw svg into an html template.
    @jinja2.contextfunction
    def include_file(ctx, name):
        env = ctx.environment
        return jinja2.Markup(env.loader.get_source(env, name)[0])

    loader = jinja2.PackageLoader(__name__, ".")
    env = jinja2.Environment(loader=loader)
    env.globals["include_file"] = include_file

    print(seasonal_arcs)

    svg = env.get_template("plate_template.svg").render(
        stroke_color="#859e6d",
        fill_color="#eafee7",
        ecliptic_stroke_color="#f5ac27;",
        RCapricorn=RadiusCapricorn,
        REquator=RadiusEquator,
        RCancer=RadiusCancer,
        place_name=place,
        latitude=latitude,
        horiz=horiz,
        azimuth_coords=azimuth_coords,
        almucantar_coords=almucantar_coords,
        ecliptic=ecliptic,
        ecliptic_divisions=ecliptic_divisions,
        ecliptic_divisions_fine=ecliptic_divisions_fine,
        ecliptic_divisions_efine=ecliptic_divisions_efine,
        aries_first_point=aries_first_point,
        aries_first_point_angle=astrolabe.obliquity,
        top_middle_outer=top_middle_outer,
        bottom_middle_outer=bottom_middle_outer,
        outer_radius=outer_radius,
        inner_radius=inner_radius,
        top_middle_inner=top_middle_inner,
        bottom_middle_inner=bottom_middle_inner,
        # ecliptic_center=ecliptic_center,
        ecliptic_pole=astrolabe.ecliptic_pole,
        seasonal_arcs=seasonal_arcs,
        stars=stars,
    )

    with open("plate.svg", "w") as fp:
        fp.write(svg)


if __name__ == "__main__":
    main()
