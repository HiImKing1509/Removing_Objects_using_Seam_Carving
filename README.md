# Removing Objects using Seam Carving
___________________________________
## Introduce

`Seam carving` (or `liquid rescaling`) is an algorithm for content-aware <a href="https://en.wikipedia.org/wiki/Image_scaling">image resizing</a>, developed by **Shai Avidan**, of <a href="https://en.wikipedia.org/wiki/Mitsubishi_Electric_Research_Laboratories">Mitsubishi Electric Research Laboratories (MERL)</a>, and Ariel Shamir, of the <a href="https://en.wikipedia.org/wiki/Interdisciplinary_Center">Interdisciplinary Center</a> and MERL. It functions by establishing a number of **seams** (paths of least importance) in an image and automatically removes seams to reduce image size or inserts seams to extend it. Seam carving also allows manually defining areas in which pixels may not be modified, and features the ability to remove whole objects from photographs.

The purpose of the algorithm is image retargeting, which is the problem of displaying images without distortion on media of various sizes (cell phones, projection screens) using document standards, like HTML, that already support dynamic changes in page layout and text but not images

## Description

| Input | Output |
|----|-----|
| ![img-original-dog1](https://user-images.githubusercontent.com/84212036/176183828-cd98af81-1ceb-4926-9de0-803cd1843500.jpg) | ![img03-final](https://user-images.githubusercontent.com/84212036/176183740-cb52637f-2aca-4058-818d-6dc28b5fb01a.png) |


## Implementation process

![SeamCarving-Seam module](https://user-images.githubusercontent.com/84212036/176184697-81be2740-1abb-419d-86bb-7de871bbe15e.png)

## Demo

![dynamicImage08](https://user-images.githubusercontent.com/84212036/176187994-c1105067-58e2-4d6f-857d-d39cf2ed08b7.gif)
