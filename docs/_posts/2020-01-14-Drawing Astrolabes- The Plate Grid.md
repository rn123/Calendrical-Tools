---
layout: post
title:  "Drawing Astrolabes: The Plate Grid"
author: Ray
---

<img src="{{ "/assets/images/astrolabe_generated_01152020.png" | relative_url }}" alt="First version of generated astrolabe image" width="25%" align="right" style="padding:5px;"/>
The plate grid of an astrolabe is the stereographic projection of the celestial sphere through the south celestial pole onto the plane of the equator. Quoting Morrison:

> The interior of the plate can be thought of as a special kind of graph paper for finding the location of celestial objects in the sky at your location. The main difference between normal graph paper and the graph paper on the plate is the lines on graph paper are normally straight while the astrolabe lines are curve. All of the curves on the astrolabe plate are drawn as arcs of circles.

Continuing, here is Morrisons basic description:

> The larger circles centered on the plate represent the Earth's tropics. The largest circle, which defines the outside of the plate, is the Tropic of Capricorn, which is the farthest south the sun ever reaches. The middle circle is the equator and the smaller circle is the sun's northern limit, the Tropic of Cancer. The circles defining the tropic are the same for all latitudes.

<img src="{{ "/assets/images/sun_in_the_church.jpg" | relative_url }}" alt="The Sun in the Church" width="25%" align="left" style="padding:5px;"/>
Not mentioned is the dependency of the plate on the obliquity of the ecliptic -- the angle that the plane of the Sun's path makes with the Earth's equator. Modern astronomy starts with the identification of the time dependence of the obliquity of the ecliptic. Drawing historically accurate diagrams needs to take into account this time dependency. The story of this discovery and how the obliquity was measured five hundred years ago appears in Heilbron's book, "The Sun in the Church." 

Morrison continues:

> The straight lines drawn as diameters of the largest circle show direction. The vertical diameter goes north and south through your location, representing your **meridian.** South is at the top and east to the left. The horizontal diameter connects east and west and is the projection of the great circle perpendicular to the meridian. It is normally called the **right horizon**, the horizon at the equator. It is perhaps easiest to visualize the plate as lying flat on a table with the top pointing south. A star chart is held overhead. You look down on an astrolabe, like a compass.

Morrison's book has details about the layout of many tools based on stereographic projections. In particular, he does have a chapter on generating star finders. Continuing with the description:

> The plate is used to find the positions of celestial objects in the sky as seen by an observer at a specific location. The interior of the plate is the stereographic projection of the tropics and the local horizontal coordinate system. The arcs on the plate represent positons in the sky. You can find anything in the sky if you know its angle above the horizon and the direction to look. The angle of something in the sky above its horizon is its **altitude** and its direction is its **azimuth.**

The easy part of drawing the plate of an astrolabe is drawing the tropics and the equator:

<img src="{{ "/assets/images/plate_grid_equation1.png" | relative_url }}" alt="equation 1" width="25%" align="left" style="padding:5px;"/>

These circles depend only on the obliquity of the ecliptic.

The circles of equal altitude (almucantars) are given by the following formulas:

<img src="{{ "/assets/images/plate_grid_equation2.png" | relative_url }}" alt="equation 2" width="25%" align="left" style="padding:5px;"/>

In particular, the radius and center for the horizon arc is obtained for an altitude of zero.

The arcs of equal azimuth are given by:
<img src="{{ "/assets/images/plate_grid_equation3.png" | relative_url }}" alt="equation 3" width="25%" align="left" style="padding:5px;"/>

<img src="{{ "/assets/images/screenshot_coding_astrolabe.png" | relative_url }}" alt="coding screenshot" width="100%" style="padding:5px;"/>
