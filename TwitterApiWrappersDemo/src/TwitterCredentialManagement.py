import os

API_KEY_ENV_VAR_NAME = "TWITTER_TRENDS_API_KEY"
API_SECRET_KEY_ENV_VAR_NAME = "TWITTTER_TRENDS_API_SECRET_KEY"
ACCESS_TOKEN_ENV_VAR_NAME = "TWITTER_TRENDS_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET_ENV_VAR_NAME = "TWITTER_TRENDS_ACCESS_TOKEN_SECRET"

missingEnvVarErrorStr = "{} environment variable is not defined"


def fetchApiCredentials():
    """
    loads standard api credentials from where they're stored in system environment variables
    :return: credentials for the standard api
    """
    apiKey = os.environ.get(API_KEY_ENV_VAR_NAME)
    assert apiKey != None, missingEnvVarErrorStr.format("API Key")

    apiSecretKey = os.environ.get(API_SECRET_KEY_ENV_VAR_NAME)
    assert apiSecretKey != None, missingEnvVarErrorStr.format("API Secret Key")

    accessToken = os.environ.get(ACCESS_TOKEN_ENV_VAR_NAME)
    assert accessToken != None, missingEnvVarErrorStr.format("API Access Token")

    accessTokenSecret = os.environ.get(ACCESS_TOKEN_SECRET_ENV_VAR_NAME)
    assert accessTokenSecret != None, missingEnvVarErrorStr.format("API Access Token Secret")

    return apiKey, apiSecretKey, accessToken, accessTokenSecret
