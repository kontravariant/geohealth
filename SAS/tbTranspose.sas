libname longdat '/folders/myshortcuts/geohealth/data/Health/LongSets/';
DATA tbwide;
	length country $ 64;
	INFILE "/folders/myshortcuts/geohealth/data/Health/tbim.csv" dsd dlm=',' firstobs=2 encoding='wlatin1';
	INPUT country $ tb2013-tb1980;
	IF country = "The former Yugoslav republic of Macedonia" then country = "The former Yugoslav Republic of Macedonia";
RUN;
PROC PRINT data=tbwide(firstobs=80 obs=150);
RUN;

DATA longdat.tblong;
	set tbwide;
	
	array atbim(1980:2013) tb1980-tb2013;
	do year = 1980 to 2013;
		tb = atbim(year);
		OUTPUT;
	END;
	drop tb2013-tb1980;
	
RUN;
PROC PRINT data=longdat.tblong(firstobs=70 obs=120);
RUN;
PROC EXPORT data=longdat.tblong
	outfile= '/folders/myshortcuts/geohealth/data/Health/LongSets/tblong.csv'
	dbms=csv
	replace;
RUN;