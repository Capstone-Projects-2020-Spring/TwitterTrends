import os

API_KEY_ENV_VAR_NAME = "TWITTER_TRENDS_API_KEY"
API_SECRET_KEY_ENV_VAR_NAME = "TWITTER_TRENDS_API_SECRET_KEY"
ACCESS_TOKEN_ENV_VAR_NAME = "TWITTER_TRENDS_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET_ENV_VAR_NAME = "TWITTER_TRENDS_ACCESS_TOKEN_SECRET"

missingEnvVarErrorStr = "{} environment variable is not defined"


def fetchApiCredentials():
    """
    loads standard api credentials from where they're stored in system environment variables
    :return: credentials for the standard api
    """

    """
    apiKey = "d4L3VAamXt6ocQIYgPOl62Irz"
    assert apiKey != None, missingEnvVarErrorStr.format("API Key")

    apiSecretKey = "j20OhYUrtrOLGTZ01edYwzFh0nh7GIVUO2xhLlt94WyEaVwU0W"
    assert apiSecretKey != None, missingEnvVarErrorStr.format("API Secret Key")

    accessToken = "942781891714932738-x5UlXEbzCxHvaShdqn9H2XRvlTnkbQf"
    assert accessToken != None, missingEnvVarErrorStr.format("API Access Token")

    accessTokenSecret = "MLL9ypOh24XYv4iyaRtmzgdCNrLZvJJu003akIFn6PEuj"
    assert accessTokenSecret != None, missingEnvVarErrorStr.format("API Access Token Secret")

    """
    apiKey = os.environ.get(API_KEY_ENV_VAR_NAME)
    assert apiKey != None, missingEnvVarErrorStr.format("API Key")

    apiSecretKey = os.environ.get(API_SECRET_KEY_ENV_VAR_NAME)
    assert apiSecretKey != None, missingEnvVarErrorStr.format("API Secret Key")

    accessToken = os.environ.get(ACCESS_TOKEN_ENV_VAR_NAME)
    assert accessToken != None, missingEnvVarErrorStr.format("API Access Token")

    accessTokenSecret = os.environ.get(ACCESS_TOKEN_SECRET_ENV_VAR_NAME)
    assert accessTokenSecret != None, missingEnvVarErrorStr.format("API Access Token Secret")


    print(apiKey)
    print(apiSecretKey)
    print(accessToken)
    print(accessTokenSecret)

    return apiKey, apiSecretKey, accessToken, accessTokenSecret