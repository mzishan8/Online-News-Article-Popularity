from flask import Flask, redirect, url_for, request, render_template

import Popularity
from textblob import TextBlob
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/')
def home():
	return render_template('Home.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/predict', methods= ['POST'])
def predict():
   print(request.form)
   feature=[]
   feature.append(731)
   feature.append(len(request.form["title"].split())+2)
   feature.append(len(request.form["text"].split()))
   print(len(set(request.form["text"].split())))
   print((len(request.form["text"].split()))+2)
   feature.append(len(set(request.form["text"].split()))/(len(request.form["text"].split())+13))
   feature.append(len(set(request.form["title"].split()))/len(request.form["title"].split()))
   feature.append(len(set(request.form["title"].split()))/len(request.form["title"].split()))
   feature.append(int(request.form["external_links"])+int(request.form["self_links"]));
   feature.append(int(request.form["self_links"]));
   feature.append(int(request.form["image"]));
   feature.append(int(request.form["video"]));
   words = request.form["text"].split()
   feature.append(sum(len(word) for word in words) / (len(words)+13))
   feature.append(0)
   print("Fyk")
   feature.append(1 if request.form["channel"]=="1" else 0)
   feature.append(1 if request.form["channel"]=="2" else 0)
   feature.append(1 if request.form["channel"]=="3" else 0)
   feature.append(1 if request.form["channel"]=="4" else 0)
   feature.append(1 if request.form["channel"]=="5" else 0)
   feature.append(1 if request.form["channel"]=="6" else 0)
   feature.append(int(request.form["max_external_share"]))
   feature.append(int(request.form["avg_self_share"]))
   print("Shik")
   feature.append(1 if request.form["day"]=="1" else 0)
   feature.append(1 if request.form["day"]=="2" else 0)
   feature.append(1 if request.form["day"]=="3" else 0)
   feature.append(1 if request.form["day"]=="4" else 0)
   feature.append(1 if request.form["day"]=="5" else 0)
   feature.append(1 if request.form["day"]=="6" else 0)
   feature.append(1 if request.form["day"]=="7" else 0)
   feature.append(1 if request.form["day"]=="6" or request.form["day"]=="7" else 0 )
   feature.append(TextBlob(request.form["text"]).sentiment.subjectivity)
   feature.append(TextBlob(request.form["text"]).sentiment.polarity)
   feature.append(TextBlob(request.form["title"]).sentiment.subjectivity)
   feature.append(TextBlob(request.form["title"]).sentiment.polarity)
   feature.append(abs(TextBlob(request.form["title"]).sentiment.subjectivity))
   feature.append(abs(TextBlob(request.form["title"]).sentiment.polarity))
   print(len(feature))
   result = ""
   if Popularity.predictPopularity(feature) == 1.0:
      result = "Popular"
   else:
      result = "Not Popular"
   result = "<H1> Your News Article will be " +result +"</H1>"
   return result



if __name__ == '__main__':
   app.run(debug = True)

# 'timedelta',
#  'n_tokens_title',
#  'n_tokens_content',
#  'n_unique_tokens',
#  'n_non_stop_words',
#  'n_non_stop_unique_tokens',
#  'num_hrefs',
#  'num_self_hrefs',
#  'num_imgs',
#  'num_videos',
#  'average_token_length',
#  'num_keywords',
#  'data_channel_is_lifestyle',
#  'data_channel_is_entertainment',
#  'data_channel_is_bus',
#  'data_channel_is_socmed',
#  'data_channel_is_tech',
#  'data_channel_is_world',
#  'self_reference_max_shares',
#  'self_reference_avg_sharess',
#  'weekday_is_monday',
#  'weekday_is_tuesday',
#  'weekday_is_wednesday',
#  'weekday_is_thursday',
#  'weekday_is_friday',
#  'weekday_is_saturday',
#  'weekday_is_sunday',
#  'is_weekend',
#  'global_subjectivity',
#  'global_sentiment_polarity',
#  'title_subjectivity',
#  # 'title_sentiment_polarity',
#  # 'abs_title_subjectivity',
 # 'abs_title_sentiment_polarity'