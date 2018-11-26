# crawler
Crawler_and_sentiment_analysis

## change number of articles retreive with the spider
In settings.py change variable

`CLOSESPIDER_ITEMCOUNT = 10`

## to run spider
`cd` in spiders folder. Then type in cmd line
`scrapy crawl quotes`

## to save new json file
`scrapy crawl quotes -o items.json`

## to start the inverted-index 
return to one earlier folder with `cd ..` then 
`python inv_index.py`

## to query the data -- example with Concordia since small database for now
`python query_processing.py Concordia`

the result of the query is saved in the text file named `Result_01.txt`

## files created
`dataset.txt` -- [general informations about all the files analysed]
`infoForQueries.txt` -- [url, length in words of this url]
`sentiment_for_each_url.txt`: -- [url, sentiment value for this url]