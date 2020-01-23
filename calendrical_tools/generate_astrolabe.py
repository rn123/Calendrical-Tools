#!/usr/bin/env python
# coding: utf-8

import math
from jinja2 import Template

# Flat list of all of the parts of an astrolabe. Once computed, these will be used in
# a jinja template to generate an svg diagram.
identifiers = [
    "astrolabe",
    "plate",
    "description",
    "tropics",
    "horizon",
    "axis",
    "almucantars",
    "almucantar_center",
    "azimuths",
    "prime_vertical",
    "limb",
    "limb_boundaries",
    "ticks",
    "short_ticks",
    "long_ticks",
    "rete",
    "ecliptic",
    "ecliptic_boundaries",
    "stars",
    "planets",
]


class Astrolabe:
    """A proper traveling astrolabe would have a set of plates for each
    clime, with maybe extra plates for special places.

    Morrison:
    > The earliest astrolabes, which were deeply influenced by Greek tradition,
    included plates for the latitudes of the *climates.* The climates of the world 
    were defined by Ptolemy to be the latitudes where the lenght of the longest 
    day of the year varied by one-half hour. Ptolemy calculated the latitude
    corresponding to a 15-minute difference in the length of the longest day
    (using a value of 23 degrees 51 minutes 20 seconds for the obliquity of
    the ecliptic) for 39 latitudes, which covered the Earth from the equator
    to the North Pole. The ones called the classic *climata* were for the
    half-hour differences in the longest day covering the then populated world."""

    climata = {
        "Meroe": 16.45,
        "Soene": 23.85,
        "Lower Egypt": 30.37,
        "Rhodes": 36.00,
        "Hellespont": 40.93,
        "Mid-Pontus": 45.02,
        "Mouth of Borysthinia": 48.53,
    }

    def __init__(
        self, obliquity=23.4443291, radius_capricorn=100, plate_parameters=None
    ):
        self.obliquity = obliquity
        self._obliquityRadians = math.radians((90 - self.obliquity) / 2)
        self.RadiusCapricorn = radius_capricorn
        self.plate_parameters = self.climata
        self.plate_altitudes = list(range(0, 90, 10))
        self.plate_azimuths = list(range(10, 90, 10))

        self.tropic_arcs()
        self.plates(plate_parameters=plate_parameters)

        # Parameters for layout of graduated limb.
        self.short_tick_angles = list(range(0, 361, 1))
        self.long_tick_angles = list(range(0, 375, 15))

        self.short_tick = 5
        self.long_tick = 15
        self.ticks = {
            "inner_radius": self.RadiusCapricorn,
            "center_radius": self.RadiusCapricorn + self.short_tick,
            "outer_radius": self.RadiusCapricorn + self.long_tick,
            "short_tick_angles": self.short_tick_angles,
            "long_tick_angles": self.long_tick_angles,
        }

        # Ecliptic
        self.RadiusEcliptic = (self.RadiusCapricorn + self.RadiusCancer) / 2.0
        self.yEclipticCenter = (self.RadiusCapricorn - self.RadiusCancer) / 2.0
        self.xEclipticCenter = 0.0

    def plates(self, plate_parameters=None):
        if plate_parameters is not None:
            self.plate_parameters.update(plate_parameters)

        self.plates = {}
        for location, latitude in self.plate_parameters.items():
            if location not in self.plates:
                self.plates[location] = {"location": location, "latitude": latitude}
            # Note: if different locations with same name, will overwrite.
            self.plate(location=location)

    def plate(self, location=None):
        """Compute parts for one plate"""
        plate = self.plates[location]
        plate_latitude = plate["latitude"]

        almucantars = self.almucantar_arcs(
            altitudes=self.plate_altitudes, latitude=plate_latitude
        )
        plate["almucantars"] = almucantars

        almucantar_center = self.almucantar_arc(altitude=80, latitude=plate_latitude)
        plate["almucantar_center"] = almucantar_center

        plate["horizon"] = self.horizon(latitude=plate_latitude)

        prime_vertical = self.azimuth_arc(
            azimuth=90, latitude=plate_latitude, prime=True
        )
        plate["prime_vertical"] = prime_vertical[0]  # TODO: clean this up

        azimuth_arcs = self.azimuth_arcs(latitude=plate_latitude)
        plate["azimuths"] = azimuth_arcs

    def horizon(self, latitude=None):
        radiansLatitude = math.radians(latitude)
        rHorizon = self.RadiusEquator / math.sin(radiansLatitude)
        yHorizon = self.RadiusEquator / math.tan(radiansLatitude)
        xHorizon = 0.0
        return {"cx": xHorizon, "cy": yHorizon, "r": rHorizon}

    def tropic_arcs(self):
        """ The size of an astrolabe is contolled by the radius of the
        tropic of Capricorn. Recall that the tropics represent the
        extreme positions of the sun on its path (the ecliptic) through 
        the course of a year. Summer solstice occurs when the sun reaches
        the tropic of Cancer and winter solstice when the sun reaches the
        tropic of Capricorn. The stereographic projection, from the south
        pole onto the plane of the equator, is visualized as lines from the
        south pole tracing out new curves on the plane of the equator. The
        projection sees the tropics as three concentric circles. From the 
        view of the south pole, the tropic of Capricorn is the outer circle
        and the tropic of Cancer is the inner circle.

        Plate grid equation 1, the tropics.
        R_{Equator} = R_{Capricorn} \tan(\frac{90 - \epsilon}{2}),
        R_{Cancer} = R_{Equator} \tan(\frac{90 - \epsilon}{2})
        """

        self.RadiusEquator = self.RadiusCapricorn * math.tan(self._obliquityRadians)
        self.RadiusCancer = self.RadiusEquator * math.tan(self._obliquityRadians)

    def almucantar_arc(self, altitude, latitude):
        """Generate circle of constant altitude.

        Plate grid equation 2, circles of equal altitude (almucantars).
        y_{center} &= R_{Equator}(\frac{\cos\phi}{\sin\phi + \sin a}), & 
        r_{a} &= R_{Equator} (\frac{\cos a}{\sin\phi + \sin a}) \\
        r_{U} &= R_{Equator} \cot(\frac{\phi +  a}{2}), &
        r_{L} &= -R_{Equator} \tan(\frac{\phi -  a}{2})
        """
        radiansAltitude = math.radians(altitude)
        radiansLatitude = math.radians(latitude)

        almucantorCenter = self.RadiusEquator * (
            math.cos(radiansLatitude)
            / (math.sin(radiansLatitude) + math.sin(radiansAltitude))
        )
        almucantarRadius = self.RadiusEquator * (
            math.cos(radiansAltitude)
            / (math.sin(radiansLatitude) + math.sin(radiansAltitude))
        )
        return {"alt": altitude, "cx": 0, "cy": almucantorCenter, "r": almucantarRadius}

    def almucantar_arcs(self, altitudes=None, latitude=None):
        almucantor_coords = []

        for altitude in altitudes:
            almucantor_coords.append(
                self.almucantar_arc(altitude=altitude, latitude=latitude)
            )
        return almucantor_coords

    def azimuth_arc(self, azimuth=None, latitude=None, prime=False):
        # Plate grid equation 3, circles of azimuth.
        radiansMinus = math.radians((90 - latitude) / 2.0)
        radiansPlus = math.radians((90 + latitude) / 2.0)

        yZenith = self.RadiusEquator * math.tan(radiansMinus)
        yNadir = -self.RadiusEquator * math.tan(radiansPlus)
        yCenter = (yZenith + yNadir) / 2.0
        yAzimuth = (yZenith - yNadir) / 2.0

        radiansAzimuth = math.radians(azimuth)
        xAzimuth = yAzimuth * math.tan(radiansAzimuth)
        radiusAzimuth = yAzimuth / math.cos(radiansAzimuth)

        if prime is True:
            coord_left = {"az": 90, "cx": 0, "cy": yCenter, "r": yAzimuth}
            coord_right = {"az": 90, "cx": 0, "cy": yCenter, "r": yAzimuth}
        else:
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

    def azimuth_arcs(self, latitude=None):

        azimuth_coords = []
        for azimuth in self.plate_azimuths:
            coords = self.azimuth_arc(azimuth=azimuth, latitude=latitude)
            azimuth_coords.extend(coords)
        return azimuth_coords


def main():

    plate_parameters = {"Honolulu": 21.3069}
    astrolabe = Astrolabe(plate_parameters=plate_parameters)
    plate = astrolabe.plates["Honolulu"]

    background_color = "#a3262a;"
    stroke_color = "#f5ac27;"

    # In order to place parts of the figure in Inkscape layers, need the attributes below.
    # This will cause errors, of course, in other renderers unless the inkscape namespace
    # (xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape") is included.

    # Use Inkscape extensions to svg to place different parts of astrolabe into their own layer.
    inkscape_attributes = {
        identifier: 'inkscape:label="{}" inkscape:groupmode="layer"'.format(identifier)
        for identifier in identifiers
    }

    animation_parameters = {"from": "233", "to": "233", "begin": "0s", "dur": "5s"}

    ecliptic = {
            "cx": astrolabe.xEclipticCenter,
            "cy": astrolabe.yEclipticCenter,
            "r": astrolabe.RadiusEcliptic,
            "width": 5,
        }
    outer_radius = ecliptic["r"]
    inner_radius = ecliptic["r"] - ecliptic["width"]

    top_middle_outer =    {"x":(ecliptic["cx"]), "y":(ecliptic["cy"] + outer_radius)}
    bottom_middle_outer = {"x":(ecliptic["cx"]), "y":(ecliptic["cy"] - outer_radius)}

    top_middle_inner =    {"x":(ecliptic["cx"]), "y":(ecliptic["cy"] + inner_radius)}
    bottom_middle_inner = {"x":(ecliptic["cx"]), "y":(ecliptic["cy"] - inner_radius)}

    with open("astrolabe_template.svg") as fp:
        template_text = fp.read()

    template = Template(template_text)
    svg = template.render(
        place_name=plate["location"],
        latitude=plate["latitude"],
        RCapricorn=astrolabe.RadiusCapricorn,
        REquator=astrolabe.RadiusEquator,
        RCancer=astrolabe.RadiusCancer,
        horiz=plate["horizon"],
        almucantor_coords=plate["almucantars"],
        almucantar_center=plate["almucantar_center"],
        azimuth_coords=plate["azimuths"],
        prime_vertical=plate["prime_vertical"],
        ticks=astrolabe.ticks,
        ecliptic=ecliptic,
        top_middle_outer=top_middle_outer,
        bottom_middle_outer=bottom_middle_outer,
        outer_radius=outer_radius,
        inner_radius=inner_radius,
        top_middle_inner=top_middle_inner,
        bottom_middle_inner=bottom_middle_inner,
        stroke_color=stroke_color,
        background_color=background_color,
        inkscape=inkscape_attributes,
        animation=animation_parameters,
        moons=[
            (44.142706092611434, 214.41520455448494),
            (-64.29833725607341, 244.05007530120906),
            (19.338217263234128, 274.11533327404277),
            (17.224801417675735, 304.36003467896535),
            (-64.16194195841945, 334.4763799297398),
            (-25.561893428663097, 4.203505420431007),
        ],
        suns=[
            214.41713740391424,
            244.05065884583018,
            274.1147430450437,
            304.35973321930214,
            334.47736243435793,
            4.204523538166541,
        ],
    )

    with open("astrolabe_generated.svg", "w") as fp:
        fp.write(svg)


if __name__ == "__main__":
    main()
