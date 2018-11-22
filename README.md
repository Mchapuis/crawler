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

## to start the inverted-index (still some errors there)
return to one earlier folder with `cd ..` then 
`python inv_index.py`
