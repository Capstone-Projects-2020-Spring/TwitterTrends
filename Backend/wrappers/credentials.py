import os
import searchtweets as st
import tweepy
import traceback

import wrappers.TwitterCredentialManagement as tcm


ENDPOINT_ENV_VAR = "SEARCHTWEETS_ENDPOINT"                                       

def getPremiumEndpointCreds(endpointType):
    """
    fetches credentials for some premium endpoint using an api key and secret
    which are already in the system's environment variables
    :parameter endpointType which premium endpoint to get the credentials for (30 day or full archive)
    :return credentials for some premium endpoint
    """
    os.environ[ENDPOINT_ENV_VAR] = endpointType;
    searchArgs = st.load_credentials(filename="NoCredsFile.yaml", account_type="premium", yaml_key="dummyYamlKey")
    # cleaning up this temporary environment variable to avoid causing a side effect
    del os.environ[ENDPOINT_ENV_VAR]

    return searchArgs

def getStandardTweepyTwitterCreds(accountInd= 0):

    apiKey, apiSecretKey, accessToken, accessTokenSecret = tcm.fetchApiCredentials(accountInd)

    auth = tweepy.OAuthHandler(apiKey, apiSecretKey)
    auth.set_access_token(accessToken, accessTokenSecret)

    twitterStandardAPI = tweepy.API(auth, retry_count=6, retry_delay=5, retry_errors=[500, 503, 504])

    try:
        twitterStandardAPI.verify_credentials()
        print("Twitter credentials valid for account #", accountInd)
    except Exception as e:
        print("Tweepy unable to authenticate with Twitter when trying to access account #", accountInd)
        print("Exception: ", e.__doc__, str(e))
        traceback.print_exc()

    return twitterStandardAPI