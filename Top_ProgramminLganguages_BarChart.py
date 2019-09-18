from collections import Counter
from matplotlib import pyplot as plt
import pandas as pd
 
plt.style.use('fivethirtyeight')
 
data=pd.read_csv('data.csv') 
ids=data['Responder_id']
languages_response=data['LanguagesWorkedWith']
    
language_counter=Counter()
for response in languages_response:
   language_counter.update(response.split(';'))
 
languages=[]
populariry=[]        
 
for item in language_counter.most_common(15):
    languages.append(item[0])
    populariry.append(item[1])
    
languages.reverse()
populariry.reverse()
 
plt.barh(languages,populariry)
plt.title('Top most popular languages')
plt.xlabel('People who use them')
 
plt.show()
