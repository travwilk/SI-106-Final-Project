
# coding: utf-8

# In[1]:


import requests_oauthlib #imports the web browser for the user
import json 
import sys
from collections import Counter #Counter is a dict subclass that counts hashable objects
import requests #To work with the Requests library


# In[2]:


client_key = "Pw8OaWdwGXuABBmrJZsy80OQX" 
client_secret = "ModQbiEv6rnPiJsc7gBIvuizJCCWm2eKO6RZNeGiwtJRVvY5Ix" 
if not client_secret or not client_key: #In case there is no client_secret or client_key provided.
    print("You need to fill in client_key and client_secret. See comments in the code around line 8-14.") 
    sys.exit(1)


# In[3]:


def get_tokens():
    #Obtains a request token which will identify the client.
    #Within the requests_oauthlib module there is a class called OAuth1Session.
    #There are two paramaters(-- the key, -- the secret). These correspond to the client_key and client secret found in the code above.
    #oauth is now an instance of the class OAuth1Session.

    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)
    #Where you must request a token. Visit this url.
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    
    #We must invoke fetch_request_token method of the class OAuth1Session on oauth(our instance) and it will return a dictionary.
    fetch_response = oauth.fetch_request_token(request_token_url)
    
    #Store two values from the dictionary into variables.
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')
    
    #Allows us to obtain authorization from the user to access their information.
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'

    authorization_url = oauth.authorization_url(base_authorization_url)

    print("""Please click on the URL below, 
          click on "Authorize App", 
          and then copy the authorization code and paste it below.""")
    print(authorization_url)
    
    #Copy and paste the verifier or the whole redirect url.
    verifier = input('Please input the verifier>>> ')
    
    #Allows us to obtain an access token from OAuth provider.
    #A new instance of OAuth1Session is made. More parameters are filled in.
    oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)

    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')

    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)


# In[4]:


try:
    f = open("creds.txt", 'r') #Opening and reading credentials from the file creds.txt.
    (client_key, client_secret, resource_owner_key, resource_owner_secret,
     verifier) = json.loads(f.read()) 
    f.close()
except:
    #In a case where it is not, you must get them and then save them in the file creds.txt.
    #It will also allow us to send fewer requests to the API and run the code faster.
    tokens = get_tokens()
    f = open("creds.txt", 'w') #Open and save it into a file that you can write from.
    f.write(json.dumps(tokens))
    f.close() #Must always close files.
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = tokens


# In[5]:


oauth_inst = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret)


# In[6]:


def next_page(ids_retrieved=[]):
    the_params = {'count' : 100} #100 tweets per page.
    if len(ids_retrieved) > 0: #In case the paging process already started. Subtracts one from the min of ids we got before.
        the_params['max_id'] = min(ids_retrieved) - 1 
    the_params['q'] = '#TaylorSwift'
    r = oauth_inst.get("https://api.twitter.com/1.1/search/tweets.json", 
                 params=the_params)

    return r.json()['statuses']

tweets_collected = [] #A list of the tweets collected. 
ids_collected = [] #A list of ids that are specific to each tweet.
pages = 2 #Two pages of 100 tweets which equals 200 tweets.
for _ in range(pages):
    next_results = next_page(ids_collected)
    tweets_collected += next_results #Adding the next_results to the tweets_collected list
    next_onehundred_ids = [tweet['id'] for tweet in next_results]
    ids_collected += next_onehundred_ids #Adding the next_onehundred_ids to the ids_collected list.


# In[7]:


len(next_page())


# In[8]:


len(tweets_collected)


# In[9]:


tweets_collected


# In[10]:


def vowel_finder(word): #Finds the words that begin with a vowel. 
    if word[0] in ['A','E','I','O','U','a','e','i','o','u']:
        return True
    else:
        return False


# In[11]:


vowel_finder("Olympics")


# In[12]:


def simplify_capitalize(new_word): #Takes a word and strips off any symbol or number. Then makes that word uppercase.
    for char in "?>.<,':;|{}[]_()*&^%$#@!0987654321":
        new_word = new_word.replace(char, '')
    return new_word.strip().upper() 


# In[13]:


simplify_capitalize("#Michigan!!!")


# In[14]:


class Tweet:
    stopwords = ['a','an','and','as','but','by','for','is','it','of','the','to']
    
    def __init__(self, tweet_dictionary={}):
        self.text = tweet_dictionary['text']
        self.time = tweet_dictionary['created_at']

        self.favorites = tweet_dictionary['favorite_count']
        self.retweets = tweet_dictionary["retweet_count"]
            
    def __str__(self):
        message = '''Tweet: {} \nTweeted at: {} \nFavorites: {} \nRetweets: {}'''.format(self.text,
                                                                                            self.time,
                                                                                            self.favorites,
                                                                                            self.retweets)
        return message #Returns the string that I saved in the variable message.
    
    def vowel_words(self):
        #If it doesn't exist after we return it, the list is created afterwards.
        try:
            return self.vowel_words
        except:
            self.vowel_words = []
            for term in self.text.split():
                nueva_palabra = vowel_finder(term)
                if nueva_palabra not in self.stopwords:
                    self.vowel_words.append(nueva_palabra)
            return self.vowel_words
        
    def filtered_tweet(self):
        #If it doesn't exist after we return it, the list is created afterwards. Same mechanism as vowel_words.
        try:
            return self.filtered_words
        except:
            self.filtered_words = []
            for word in self.text.split():
                new_word = simplify_capitalize(word)
                if new_word not in self.stopwords:
                    self.filtered_words.append(new_word)
            return self.filtered_words


# In[15]:


tweet_lst = [] #A list of tweet objects 
for tweet_dicts in tweets_collected: #Iterate through each dictionary in tweets_collected.
    tweet_lst.append(Tweet(tweet_dicts))

words_filtered = [] #A list of filtered words
for tweet_objects in tweet_lst: #Iterate through each tweet_object in tweet_lst.
    for term in tweet_objects.filtered_tweet(): 
        if len(term) >= 5:
            words_filtered.append(term) #Append each filterd word to the end of the list words_filtered.


# In[16]:


most_common_word = Counter(words_filtered).most_common(1)
most_common_word = most_common_word[0][0]
print(most_common_word)


# In[17]:


try:
    itunes_response = requests.get('http://itunes.apple.com/search', params={
        'term': most_common_word})
    response = json.loads(itunes_response.text) 
except:
    print('Sorry, problem making request!')


# In[18]:


song_dictionaries = []
for term in response['results']: #Iterate through all dictionaries in response['results'] 
    if term['kind'] == 'song':
        song_dictionaries.append(term) #Append the dictionary to the end of the song_dictionaries.


# In[19]:


song_dictionaries[0].keys()


# In[20]:


class Song:
    def __init__(self, song_dict={}):
        self.artist = song_dict['artistName']
        self.album = song_dict['collectionName']
        self.classification = song_dict['kind']
        self.title = song_dict['trackName']
        self.length = song_dict['trackTimeMillis'] / 1000
    def __str__(self):
        song_message = "Artist: {}. \nAlbum: {}. \nType: {}. \nTitle: {}. \nLength: {} seconds.".format(self.artist, self.album, self.classification, self.title, self.length)
                                                                                                                                                     
                                                                                                                                                                                                                                                                                               
        return song_message #Returns the string that I saved in the variable song_message.


# In[21]:


song = Song(song_dictionaries[0])


# In[22]:


lst_songs = []
for song_dictionary in song_dictionaries: #Iterate through each dictionary in song_dictionaries.
    song = Song(song_dictionary)
    lst_songs.append(song) #Append the dictionary to the end of the lst_songs.


# In[23]:


songs_sorted = sorted(lst_songs, key = lambda x: x.length, reverse = True) #Sorting songs from longest to shortest in terms of duration.


# In[24]:


import csv 
with open("song_info.csv", "w") as outfile:
    output = csv.writer(outfile, delimiter = ",")
    output.writerow(['artist', 'album','classification','title', 'length'])
    for song in songs_sorted:
        artist = song.artist
        album = song.album
        classification = song.classification
        title = song.title
        length = song.length
        output.writerow([artist, album, classification, title, length])


# In[25]:


get_ipython().system('head song_info.csv')

