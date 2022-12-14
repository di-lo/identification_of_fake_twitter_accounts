# identification_of_fake_twitter_accounts
## AI4ALL Portfolio Project Summer 2022

Social media platforms have been entirely an undeniable part of the lifestyle for the past decade. Analyzing the information being shared is a crucial step to understanding how social media works. By analyzing the text similarity, media content, and published time, I can find the fake accounts according to the comparison of the timeline and similarity percent. Additionally, I can analyze how the media controls us.

**Comparison of Elon Musk’s Real Account and Alleged Fake Account**

<img width="400" alt="product" src="https://user-images.githubusercontent.com/60364755/197367113-62d7e899-997e-496f-96a5-212d548c6234.png">

### Data

Firstly, the timeline of each profile has been extracted using the official TwitterAPI. 
In according to access TwitterAPI, I had to access Twitter's Developer Platform which enables me to access the power of Twitter's open, global, real-time, and historical platform. Then, all information is given to the proposed system.

### Model/Algorithm 

In parallel, three aspects (text, media, hours) of a profile are derived. Behavioral ratios are time-series-related information showing the consistency and habits of the user. Dynamic time warping has been utilized for the comparison of the behavioral ratios of the two profiles. Next, the audience network is extracted for each user, and for estimating the similarity of the two sets. Finally, for the Content similarity measurement, the tweets are preprocessed respecting the feature extraction method; TF-IDF and DistilBERT for feature extraction are employed and then compared using the cosine similarity method for similarity in text analysis. Additionally, I used deepai.org API to detect the similarities between media.

![AI4ALL Portfolio Project_ Twitter Accounts Comparison pptx](https://user-images.githubusercontent.com/60364755/197378704-655f5128-48c7-4367-9d8c-ddccb66ca505.jpg)
