# Millet disease detection api
The api consists a post request end-point to accept an image and detect the millet's disease in the image.

This is the back-end part of the two-part-system of Millet disease detection. The fron-end app part can be found at-
[Millet app for disease detection](https://github.com/pratikg1999/millet_app "Millet app")


## Working
An image is taken via post request. First, it is tested whether plant is present in the image. If plant is present, it is run on our trained model of detecting the plant disease.
The disease along with it probability is sent to the client (in JSON format).

## Technologies used
* Django rest
* ResNet
* GoogLeNet

## Useful links
* [Millet app for disease detection](https://github.com/pratikg1999/millet_app "Millet app")
* [Millet disease detection project report](https://github.com/pratikg1999/millet_app/blob/master/Millet_Disease_Detection_Minor_Report%20(2).pdf "Millet disease detection report")
* [Millet disease detection presentation](https://github.com/pratikg1999/millet_app/blob/master/Minor%20Project.pptx "Millet disease detection ppt")

