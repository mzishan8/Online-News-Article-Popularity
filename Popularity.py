import findspark
findspark.init('/home/zishan/spark-2.2.1-bin-hadoop2.7')
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('Popularity').getOrCreate()
data = spark.read.csv('OnlineNewsPopularity.csv',inferSchema=True,header=True)
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.feature import VectorAssembler
assembler = VectorAssembler(inputCols=['timedelta',
 'n_tokens_title',
 'n_tokens_content',
 'n_unique_tokens',
 'n_non_stop_words',
 'n_non_stop_unique_tokens',
 'num_hrefs',
 'num_self_hrefs',
 'num_imgs',
 'num_videos',
 'average_token_length',
 'num_keywords',
 'data_channel_is_lifestyle',
 'data_channel_is_entertainment',
 'data_channel_is_bus',
 'data_channel_is_socmed',
 'data_channel_is_tech',
 'data_channel_is_world',
 'self_reference_max_shares',
 'self_reference_avg_sharess',
 'weekday_is_monday',
 'weekday_is_tuesday',
 'weekday_is_wednesday',
 'weekday_is_thursday',
 'weekday_is_friday',
 'weekday_is_saturday',
 'weekday_is_sunday',
 'is_weekend',
 'global_subjectivity',
 'global_sentiment_polarity',
 'title_subjectivity',
 'title_sentiment_polarity',
 'abs_title_subjectivity',
 'abs_title_sentiment_polarity'],outputCol='features' )
new_data = assembler.transform(data)


final_data = new_data.select('features','shares')
from pyspark.ml.feature import QuantileDiscretizer
discretizer = QuantileDiscretizer(numBuckets=2, inputCol="shares", outputCol="result")
result = discretizer.fit(final_data).transform(final_data)
finalData = result.select('result','features')
from pyspark.ml.classification import RandomForestClassifier
rfc = RandomForestClassifier(numTrees=250,labelCol='result',featuresCol='features')
train_data,test_data = finalData.randomSplit([0.7,0.3])
rfc_model = rfc.fit(train_data)
result = rfc_model.transform(test_data);
from pyspark.ml.evaluation import BinaryClassificationEvaluator
acc_eval = BinaryClassificationEvaluator(labelCol='result')
print(acc_eval.evaluate(result))
test_data.head(1)


# import os, sys
# import pandas
# import plotly.plotly as py
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# import cufflinks as cf
# import plotly.graph_objs as go
# init_notebook_mode(connected=True)
# sys.path.append("".join([os.environ["HOME"]])) 
# result.columns
# predictions_pdf = result.select('result', 'features', 'rawPrediction', 'probability', 'prediction').toPandas()
# cumulative_stats = predictions_pdf.groupby(['prediction']).count()
# product_data = [go.Pie(labels=cumulative_stats.indexGENDER, values=cumulative_stats['features'])]
# product_layout = go.Layout(title='Predicted product line client interest distribution')
# fig = go.Figure(data=product_data, layout=product_layout)
# iplot(fig)
#test_data.show()


unlabel_data = test_data.select('features')
res = rfc_model.transform(unlabel_data)

# inputData = []
# for i in range(0, 34):
#     inputData.append(i * i +0.432);

def predictPopularity(features):
    print(features)
    features = tuple(features)
    feature_label = []    
    for i in range(0, len(features)):
        feature_label.append('feature' +str(i))
    data_frame = spark.createDataFrame([features], feature_label)
    assembler = VectorAssembler(inputCols= feature_label, outputCol = 'features')
    data_frame = assembler.transform(data_frame)
    data_frame = data_frame.select('features')
    result = rfc_model.transform(data_frame)
    return result.select('prediction').head(1)[0][0]


# In[291]:


# print(predictPopularity(inputData))

