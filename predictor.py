from pyspark.sql import *
from pyspark.ml import PipelineModel
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StringIndexer, VectorIndexer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import util

spark = SparkSession.builder.appName('Demo').getOrCreate()

model = PipelineModel.load("gbtregressor.model")


analyzer = SentimentIntensityAnalyzer()
def sentiment_analyze(text, flag):
    vs = analyzer.polarity_scores(text)
    return vs[flag]


def predict(doc):
    tweet = Row(source=doc['source'], 
                retweet_count=doc['retweet_count'], 
                favorite_count=doc['favorite_count'], is_retweet=doc['is_retweet'],
                sentiment_compound=sentiment_analyze(doc['text'], "compound"),
                sentiment_neg=sentiment_analyze(doc['text'], "neg"),
                sentiment_neu=sentiment_analyze(doc['text'], "neu"),
                sentiment_pos=sentiment_analyze(doc['text'], "pos"),
                hour=util.convertUTCtoHourOfDay(doc['created_at']),
                day=util.convertUTCtoDay(doc['created_at']),
                week=util.convertUTCtoWeekNumber(doc['created_at']),
                month=util.convertUTCtoMonth(doc['created_at']),
                year=util.convertUTCtoYear(doc['created_at'])
            )
    tweet_df = spark.createDataFrame([tweet])
    
    str_indexer = StringIndexer().setInputCol("source").setOutputCol("source_index").fit(tweet_df)
    tweet_df2 = str_indexer.transform(tweet_df)
    tweet_df3 = tweet_df2.select([col(c).cast("double").alias(c) for c in tweet_df2.columns])
    predictions = model.transform(tweet_df3)
    result = predictions.select("prediction").collect()
    
    if len(result)>0:
        return result[0]['prediction']
    
    return None