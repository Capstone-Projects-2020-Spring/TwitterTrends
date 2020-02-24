import os

import searchtweets as st

ENDPOINT_ENV_VAR = "SEARCHTWEETS_ENDPOINT"

TWITTER_PREMIUM_API_ENDPOINT_FORMAT = "https://api.twitter.com/{}/tweets/search/{}/{}.json"
TWITTER_API_VERSION = "1.1"
MONTH_SEARCH_PRODUCT = "30day"
FULL_ARCHIVE_SEARCH_PRODUCT = "fullarchive"
MONTH_SEARCH_DEV_ENV_LABEL = "SSBase30DayEnv"
FULL_ARCHIVE_SEARCH_DEV_ENV_LABEL = "SSBaseFullArchiveEnv"

PREMIUM_30_DAY_ENDPOINT = TWITTER_PREMIUM_API_ENDPOINT_FORMAT.format(TWITTER_API_VERSION, MONTH_SEARCH_PRODUCT,
                                                                     MONTH_SEARCH_DEV_ENV_LABEL)
PREMIUM_FULL_ARCHIVE_ENDPOINT = TWITTER_PREMIUM_API_ENDPOINT_FORMAT.format(TWITTER_API_VERSION,
                                                                           FULL_ARCHIVE_SEARCH_PRODUCT,
                                                                           FULL_ARCHIVE_SEARCH_DEV_ENV_LABEL)


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


if __name__ == '__main__':
    print("running search-tweets demo program")
    monthSearchArgs = getPremiumEndpointCreds(PREMIUM_30_DAY_ENDPOINT)

    # max_results must stay 100 b/c we're using a sandbox account
    coronavirusRule = st.gen_rule_payload("lang:en coronavirus", from_date="2020-02-01")
    tweets = st.collect_results(coronavirusRule, max_results=100, result_stream_args=monthSearchArgs)
    [print(tweet.all_text, end="\n") for tweet in tweets[0:50]]
