DATA measleswide;
	length code $ 3; length country $ 32;
	INFILE "/folders/myshortcuts/geohealth/data/Health/Measles_pct_immune_1yo_codes.csv" dsd dlm=',' firstobs=2 encoding='wlatin1';
	INPUT code $ country $ m2013-m1980;
RUN;
PROC PRINT data=measleswide (obs=30);
RUN;
DATA longdat.measleslong;
set measleswide;
	
	array amim(1980:2013) m1980-m2013;
	do year = 1980 to 2013;
		mim = amim(year);
		OUTPUT;
	end;
	drop m1980-m2013;
RUN;
PROC PRINT data=longdat.measleslong (obs=68);
RUN;
PROC EXPORT data= longdat.measleslong
	outfile = '/folders/myshortcuts/geohealth/data/Health/LongSets/measleslong.csv'
	dbms=csv
	replace;
RUN;