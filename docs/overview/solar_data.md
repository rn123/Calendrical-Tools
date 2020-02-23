# Solar Observation Data

<img src="{{ "/assets/images/gb_gBAAnTXm89EC_000103.png" | relative_url }}" alt="data" width="100%" style="padding:5px;"/>

{% highlight python %}
iimport cv2
import numpy as np

sigma=0.33
file = "images/bub_gb_gBAAnTXm89EC_images/gb_gBAAnTXm89EC_000108.png"
file = "images/bub_gb_gBAAnTXm89EC_images/gb_gBAAnTXm89EC_000364.png"
img = cv2.imread(file, 0)
(thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)

## Invert the image

img_bin = 255 - img_bin

## Defining a kernel length

horiz_kernel_length = np.array(img).shape[0]//200
vert_kernel_length = np.array(img).shape[1]//150

## Detect horizontal lines

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horiz_kernel_length, 1))

detect_horizontal = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, horizontal_kernel, iterations=3)

## Detect vertical lines

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vert_kernel_length))
detect_vertical = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vertical_kernel, iterations=3)

## A kernel of (3 X 3) ones

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

## Weighting parameters, this will decide the quantity of an image to be added to make a new image

alpha = 0.5
beta = 1.0 - alpha

img_final_bin = cv2.addWeighted(detect_vertical, alpha, detect_horizontal, beta, 0.0)
img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
(thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img_final_bin, contours=contours, contourIdx=-1, color=(23,255,23),
thickness=3)
cv2.imwrite('detecttable.jpg', img)
{% endhighlight %}

<img src="{{ "/assets/images/detecttable.png" | relative_url }}" alt="data" width="100%" style="padding:5px;" align="right"/>
