#!/usr/bin/env python
# coding: utf-8

import math
from jinja2 import Template

# All of the parts of an astrolabe.
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


def generate_tropic_arcs(obliquity, radius_capricorn):
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

    radians = math.radians((90 - obliquity) / 2)
    radius_equator = radius_capricorn * math.tan(radians)
    radius_cancer = radius_capricorn * math.tan(radians)

    return radius_equator, radius_cancer


def generate_almucantar_arc(altitude, radius_equator, latitude):
    """Generate circles of constant altitude."""

    # Plate grid equation 2, circles of equal altitude (almucantars).
    radiansAltitude = math.radians(altitude)
    radiansLatitude = math.radians(latitude)

    almucantorCenter = radius_equator * (
        math.cos(radiansLatitude)
        / (math.sin(radiansLatitude) + math.sin(radiansAltitude))
    )
    almucantarRadius = radius_equator * (
        math.cos(radiansAltitude)
        / (math.sin(radiansLatitude) + math.sin(radiansAltitude))
    )
    return {"alt": altitude, "cx": 0, "cy": almucantorCenter, "r": almucantarRadius}


def main():
    # Obliquity of the ecliptic.
    epsilon = 23.438446
    RadiusCapricorn = 100

    # Honolulu: 21.3069° N, 157.8583° W, HST = GMT - 10
    place_name = "Honolulu"
    latitude = 21.3069
    radiansLatitude = math.radians(latitude)

    RadiusEquator, RadiusCancer = generate_tropic_arcs(
        obliquity=epsilon, radius_capricorn=RadiusCapricorn
    )

    almucantor_coords = []
    altitudes = list(range(0, 90, 10))
    for altitude in altitudes:
        almucantor_coords.append(
            generate_almucantar_arc(
                altitude=altitude, radius_equator=RadiusEquator, latitude=latitude
            )
        )

    almucantar_center = generate_almucantar_arc(
        altitude=80, radius_equator=RadiusEquator, latitude=latitude
    )

    rHorizon = RadiusEquator / math.sin(radiansLatitude)
    yHorizon = RadiusEquator / math.tan(radiansLatitude)
    xHorizon = 0.0

    # Plate grid equation 3, circles of azimuth.
    azimuth_coords = []

    yZenith = RadiusEquator * math.tan(math.radians(90 - latitude) / 2.0)
    yNadir = -RadiusEquator * math.tan(math.radians(90 + latitude) / 2.0)
    yCenter = (yZenith + yNadir) / 2.0
    yAzimuth = (yZenith - yNadir) / 2.0
    degrees = list(range(10, 90, 10))
    for azimuth in degrees:
        radiansAzimuth = math.radians(azimuth)
        xAzimuth = yAzimuth * math.tan(radiansAzimuth)
        radiusAzimuth = yAzimuth / math.cos(radiansAzimuth)
        coord = {"az": azimuth, "cx": xAzimuth, "cy": yCenter, "r": radiusAzimuth}
        azimuth_coords.append(coord)
        coord = {"az": azimuth, "cx": -xAzimuth, "cy": yCenter, "r": radiusAzimuth}
        azimuth_coords.append(coord)

    prime_vertical = {"cx": 0, "cy": yCenter, "r": yAzimuth}

    # Parameters for layout of graduated limb.
    short_tick_angles = list(range(0, 361, 1))
    long_tick_angles = list(range(0, 375, 15))

    short_tick = 5
    long_tick = 15
    ticks = {
        "inner_radius": RadiusCapricorn,
        "center_radius": RadiusCapricorn + short_tick,
        "outer_radius": RadiusCapricorn + long_tick,
        "short_tick_angles": short_tick_angles,
        "long_tick_angles": long_tick_angles,
    }

    # Ecliptic
    RadiusEcliptic = (RadiusCapricorn + RadiusCancer) / 2.0
    yEclipticCenter = (RadiusCapricorn - RadiusCancer) / 2.0
    xEclipticCenter = 0.0

    # In order to place parts of the figure in Inkscape layers, need the attributes below.
    # This will cause errors, of course, in other renderers unless the inkscape namespace
    # (xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape") is included.

    # Use Inkscape extensions to svg to place different parts of astrolabe into their own layer.
    inkscape_attributes = {
        identifier: 'inkscape:label="{}" inkscape:groupmode="layer"'.format(identifier)
        for identifier in identifiers
    }

    animation_parameters = {"from": "0", "to": "233", "begin": "0s", "dur": "5s"}

    with open("astrolabe_template.svg") as fp:
        template_text = fp.read()

    template = Template(template_text)
    svg = template.render(
        place_name=place_name,
        latitude=latitude,
        RCapricorn=RadiusCapricorn,
        REquator=RadiusEquator,
        RCancer=RadiusCancer,
        horiz={"cx": xHorizon, "cy": yHorizon, "r": rHorizon},
        almucantor_coords=almucantor_coords,
        almucantar_center=almucantar_center,
        azimuth_coords=azimuth_coords,
        prime_vertical=prime_vertical,
        ticks=ticks,
        ecliptic={
            "cx": xEclipticCenter,
            "cy": yEclipticCenter,
            "r": RadiusEcliptic,
            "width": 5,
        },
        inkscape=inkscape_attributes,
        animation=animation_parameters,
    )

    with open("astrolabe_generated.svg", "w") as fp:
        fp.write(svg)


if __name__ == "__main__":
    main()
