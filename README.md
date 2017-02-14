# geohealth
#### with a small 'g'
Retrospective broad analysis of national health and economic indicators.



**Statistical Philosophy and investigative paradigm:**

[Vashishth Statistics: 'Some Reflections on Teaching'](http://vasishth-statistics.blogspot.com/2015/08/some-reflections-on-teaching.html)

**Reproduction Philosophy**

Based on ['cookiecutter data science' ](https://drivendata.github.io/cookiecutter-data-science/) paradigm

Reproducibility being formulated in project/ subfolder as the study progresses. Liberties taken, NOTED IN project/README.md
* *doc* is documentation notes and notebooks
* *data* is raw data files
* *models* is trained and/or serialized models, predictions and summaries
* *src* is source code to run the entire project (*chronological/logical order of both creation & execution*)
    * *data* is scripts to download or generate raw data
    * *munge* is code to format, combine and melt/cast raw data files, and create features from that data
    * *model* contains scripts to train model and run predictions
    * *visualization* scripts produce graphics
* Makefile is used to initiate, clean up/roll back edits and otherwise run the project from start to finish.
    * parameters allow for pause at certain stages to conduct independent analysis/examination of data.
    
    
**Citation:**

* Feenstra, Robert C., Robert Inklaar and Marcel P. Timmer (2015), "The Next Generation of the Penn World Table" forthcoming American Economic Review, available for download at www.ggdc.net/pwt

* *Data from:*
    * [World Health Organization](www.who.int)
    * [Penn World Tables 9.0](www.rug.nl/research/ggdc/data/pwt/pwt-9.0)
    * [World bank world development indicators](http://data.worldbank.org/data-catalog/world-development-indicators)
