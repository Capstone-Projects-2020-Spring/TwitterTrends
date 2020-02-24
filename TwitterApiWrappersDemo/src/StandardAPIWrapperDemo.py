import tweepy

import src.TwitterCredentialManagement as tcm

TEST_TWITTER_USERNAME = "ScottSSalisbur1"

if __name__ == '__main__':
    print("running tweepy demo program")

    apiKey, apiSecretKey, accessToken, accessTokenSecret = tcm.fetchApiCredentials()

    auth = tweepy.OAuthHandler(apiKey, apiSecretKey)
    auth.set_access_token(accessToken, accessTokenSecret)

    twitterStandardApi = tweepy.API(auth)

    try:
        twitterStandardApi.verify_credentials()
        print("Twitter credentials valid")
    except:
        print("Tweepy unable to authenticate with Twitter")

    user = twitterStandardApi.get_user(TEST_TWITTER_USERNAME)
    print("Test User Details:")
    print("Account creation date= " + str(user.created_at))
    print("ID String= " + user.id_str)


    print("\n\nTrend information:")
    worldwideLocCode= 1
    trendsResult = twitterStandardApi.trends_place(worldwideLocCode)
    for trend in trendsResult[0]["trends"]:
        trendName = trend["name"]
        trendPop = trend["tweet_volume"]
        if trendPop is None:
            trendPop = "unknown number of"
        else:
            trendPop = str(trendPop)

        print("Trend " + trend["name"] + " was used in " + trendPop + " tweets")
