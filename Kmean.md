Kmeans Classification
========================================================


```r
library(raster)
library(maptools)
library(ggplot2)
library(plyr)
library(reshape2)
library(rgdal)
```

#Goals

##Read in points

Georeferenced points relating to the classes


```r
pts<-read.csv("C:/Users/thompson/Desktop/Whetstone_groundtruth_landscapefeatures3.csv")
```

Basic descriptive data on the classes


```r
table(pts$Landscape.class)
```

```
## 
##   bush  hummock   swale    tree 
##      37      22      72      10
```

Turn into spatial class


```r
pts<-SpatialPointsDataFrame(cbind(pts$UTM1,pts$UTM2),pts)
```

Set to utm


```r
proj4string(pts)<-"+proj=utm +zone=10 ellps=WGS84"
```


```r
ptsll<-spTransform(pts,CRS("+proj=longlat +datum=WGS84"))
```

Overlay points on our cutout


```r
plot(rcrop)
```

```
## Error in plot(rcrop): error in evaluating the argument 'x' in selecting a method for function 'plot': Error: object 'rcrop' not found
```

```r
points(ptsll,col="black",cex=20)
```

```
## Error in plot.xy(xy.coords(x, y), type = type, ...): plot.new has not been called yet
```

Draw extent of points


```r
e<-extent(ptsll)
```

##Read in the raster 
crop by extent of points

```r
r<-raster("G:/Serenity/ImageProcessing/AgisoftFull20150425_Run3.tif")
rcrop<-crop(r,e)
plot(rcrop)
```

![plot of chunk unnamed-chunk-9](figure/unnamed-chunk-9-1.png) 

#Overlay points

```r
plot(rcrop)
points(ptsll,col=ptsll$Landscape.class,pch=16,cex=1.5)
```

![plot of chunk unnamed-chunk-10](figure/unnamed-chunk-10-1.png) 

##Extract points from the raster


```r
names(rcrop)<-"Drone"
vals<-extract(x=rcrop,y=ptsll,sp=T)
```

Let's learn about the values


```r
ggplot(vals@data,aes(x=Landscape.class,y=Drone)) + geom_boxplot() + theme_bw()
```

```
## Warning in loop_apply(n, do.ply): Removed 1 rows containing non-finite
## values (stat_boxplot).
```

![plot of chunk unnamed-chunk-12](figure/unnamed-chunk-12-1.png) 

Grab some random points and plot


```r
rval<-data.frame(Landscape.class="Random",vals=sampleRandom(rcrop,10000))
```

Plot the distribution of values against classes


```r
f2<-rbind.fill(f,rval)
```

```
## Error in rbind.fill(f, rval): object 'f' not found
```

```r
ggplot(f2,aes(x=Landscape.class,y=vals)) + geom_boxplot() + theme_bw()
```

```
## Error in ggplot(f2, aes(x = Landscape.class, y = vals)): object 'f2' not found
```

```r
ggplot(f2,aes(x=vals,fill=Landscape.class)) + geom_density(alpha=.3) + theme_bw()
```

```
## Error in ggplot(f2, aes(x = vals, fill = Landscape.class)): object 'f2' not found
```

## Classify points

##Kmeans classification

## Project raster

