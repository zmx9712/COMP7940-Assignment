# Chatbot Required Features


This is line chatbot.


The line chatbot is the context of public health care about the coronavirus.

1. The bot should be able to differentiate 3 different types of queries and give 3 different types of
responses.
2. The bot should use a redis server to store some persistent information.
3. The bot should use consume another service other than redis.
4. The bot should be running on Heroku.
5. The bot should use git for version controls.
6. The LINE bot should be written only with Python and its library.


# Chatbot function design
1.Function in showing knowledge about coranavirus. This function will be performed through direct display or Q & A. 
  After users query the key word coronavirusknowledge, the chatbot will return the latest knowledge about coronvirus and the link go ahead to the web page. If users query the key word Q&A, the chatbot will return about 5 questions related to coronavirus. Users can input their answer and the chatbot will return the feedback.
  
