#!/usr/bin/env python
# coding: utf-8

import math
from jinja2 import Template

epsilon = 23.438446
latitude = 21.5767  # Waialua
RadiusCapricorn = 100

radiansLatitude = math.radians(latitude)

# Plate grid equation 1, the tropics.
# R_{Equator} = R_{Capricorn} \tan(\frac{90 - \epsilon}{2}),
# R_{Cancer} = R_{Equator} \tan(\frac{90 - \epsilon}{2})
radians = math.radians((90 - epsilon) / 2)
RadiusEquator = RadiusCapricorn * math.tan(radians)
RadiusCancer = RadiusEquator * math.tan(radians)


# Plate grid equation 2, circles of latitude (almucantars).
almucantor_coords = []
degrees = list(range(2, 62, 2)) + list(range(60, 85, 5))
for altitude in degrees:
    radiansAltitude = math.radians(altitude)
    almucantorCenter = RadiusEquator * (
        math.cos(radiansLatitude)
        / (math.sin(radiansLatitude) + math.sin(radiansAltitude))
    )
    almucantarRadius = RadiusEquator * (
        math.cos(radiansAltitude)
        / (math.sin(radiansLatitude) + math.sin(radiansAltitude))
    )
    almucantor_coords.append(
        {"alt": altitude, "cx": 0, "cy": almucantorCenter, "r": almucantarRadius}
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


# Use Inkscape extensions to svg to place different parts of astrolabe into their own layer.
identifiers = [
    "astrolabe",
    "plate",
    "tropics",
    "horizon",
    "almucantars",
    "azimuths",
    "limb",
    "limb_boundaries",
    "ticks",
    "short_ticks",
    "long_ticks",
    "ecliptic",
    "ecliptic_boundaries",
]

inkscape_attributes = {
    identifier: 'inkscape:label="{}" inkscape:groupmode="layer"'.format(identifier)
    for identifier in identifiers
}

animation_parameters = {"from": "0", "to": "233", "begin": "0s", "dur": "5s"}

with open("astrolabe_template.svg") as fp:
    template_text = fp.read()

template = Template(template_text)
svg = template.render(
    RCapricorn=RadiusCapricorn,
    REquator=RadiusEquator,
    RCancer=RadiusCancer,
    horiz={"cx": xHorizon, "cy": yHorizon, "r": rHorizon},
    almucantor_coords=almucantor_coords,
    azimuth_coords=azimuth_coords,
    ticks=ticks,
    ecliptic={"cx": xEclipticCenter, "cy": yEclipticCenter, "r": RadiusEcliptic, "width": 5},
    inkscape=inkscape_attributes,
    animation=animation_parameters,
)

with open("astrolabe_generated.svg", "w") as fp:
    fp.write(svg)
