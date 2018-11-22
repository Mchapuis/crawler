# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from afinn import Afinn
import json


class ScrapycrawlerPipeline(object):

    def process_item(self, item, spider):
        """
        afinn = Afinn()
        scored_text = afinn.score(item["text"])
        item["sentiment"] = scored_text
        return item
        """

