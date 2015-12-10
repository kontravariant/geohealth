libname longdat "/folders/myshortcuts/geohealth/data/Health/LongSets/";

DATA tbmeas;
merge longdat.measleslong longdat.tblong;
RUN;
PROC PRINT data=tbmeas;
RUN;