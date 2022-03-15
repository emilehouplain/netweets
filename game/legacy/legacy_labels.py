    labels2=[]
    firstTweet2=Dict['compteTwitter'].tweet_set.order_by('created_at')[0]
    lastTweet2=Dict['compteTwitter'].tweet_set.order_by('-created_at')[0] #tweet le plus ancien

    labels2.append([firstTweet2.created_at.month,firstTweet2.created_at.year]) #A changer pour que ca donne Month/Year[2:4]
    while firstTweet2.created_at != lastTweet2.created_at :
        date = firstTweet2.created_at
        date.month = date.month+relativedelta(months=1)
        labels2.append([firstTweet2.created_at.month,firstTweet2.created_at.year])


    labels=[]
    firstTweet=Dict['compteTwitter'].tweet_set.order_by('created_at')[0]
    lastTweet=Dict['compteTwitter'].tweet_set.order_by('-created_at')[0] #tweet le plus ancien
    dateFirstTweet=firstTweet.created_at
    dateLastTweet=lastTweet.created_at
    monthFirstTweet=firstTweet.created_at.month
    yearFirstTweet=firstTweet.created_at.year
    monthLastTweet=lastTweet.created_at.month
    yearLastTweet=lastTweet.created_at.year

    i=True


    month=monthFirstTweet
    year=yearFirstTweet

    while i==True : #Première année
        while month < 13 :
            labels.append([month,year]) #A changer pour que ca donne Month/Year[2:4]
            month=month+1
        i=False
        month=0
        year=year+1
    
    while year<yearLastTweet : #Années du milieu
        while month<12 :
            month=month+1
            labels.append([month,year])
        month=0
        year=year+1

    while month < monthLastTweet : 
        month=month+1
        labels.append([month,year])
