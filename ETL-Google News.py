
from GoogleNews import GoogleNews 
import pandas as pd
gNews = GoogleNews(period='5d')
gNews.search("bac")
result = gNews.result()
data = pd.DataFrame.from_dict(result)
data = data.drop(columns=["img"])
data.head()

for res in result:
    print("Title:", res["title"])
    print("Details:", res["link"])