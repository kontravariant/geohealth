libname dat "/folders/myshortcuts/geohealth/SAS/data/";
libname longdat "/folders/myshortcuts/geohealth/data/Health/LongSets";
DATA ccodes;
	length country $ 64;
	INFILE "/folders/myshortcuts/geohealth/countrycodes.csv" dsd dlm="," firstobs=3 encoding="utf-8";
	INPUT num country $ code $;
	
	text1 = country;
	Country_cleaned = upcase(prxchange('s/ I | in | a | the | of|\(([^)]*)\)//i',-1,strip(text1)));
	drop text1 country;
	
RUN;
PROC PRINT data=ccodes;
RUN;
PROC SORT data=ccodes;
	by country_cleaned;
RUN;
PROC SORT data=longdat.tblong out=tblongsort;
	by country;
RUN;

DATA work.tblongsort;
set tblongsort;
	country_cleaned = upcase(prxchange('s/ I | in | a | the | of|\(([^)]*)\)//i',-1,strip(country)));
	drop country;

DATA longdat.tbcodes;
	merge ccodes tblongsort;
		by country_cleaned;
		
	if year = . then delete;
run;
PROC PRINT data=longdat.tbcodes;
RUN;