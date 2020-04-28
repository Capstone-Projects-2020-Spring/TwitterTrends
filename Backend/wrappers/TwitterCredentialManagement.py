import os

API_KEY_ENV_VAR_NAME = "TWITTER_TRENDS_{}_API_KEY"
API_SECRET_KEY_ENV_VAR_NAME = "TWITTER_TRENDS_{}_API_SECRET_KEY"
ACCESS_TOKEN_ENV_VAR_NAME = "TWITTER_TRENDS_{}_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET_ENV_VAR_NAME = "TWITTER_TRENDS_{}_ACCESS_TOKEN_SECRET"

missingEnvVarErrorStr = "{} environment variable {} is not defined"


def fetchApiCredentials(accountInd):
    """
    loads one Twitter developer account's standard api credentials
    from where they're stored in system environment variables
    :param accountInd: which twitter developer account's credentials to retrieve
    :return: credentials for the standard api
    """

    accountIndStr = str(accountInd)

    currApiKeyEnvVar = API_KEY_ENV_VAR_NAME.format(accountIndStr)
    apiKey = os.environ.get(currApiKeyEnvVar)
    assert apiKey != None, missingEnvVarErrorStr.format("API Key", accountIndStr)

    currApiSecretKeyEnvVar = API_SECRET_KEY_ENV_VAR_NAME.format(accountIndStr)
    apiSecretKey = os.environ.get(currApiSecretKeyEnvVar)
    assert apiSecretKey != None, missingEnvVarErrorStr.format("API Secret Key", accountIndStr)

    currAccessTokenEnvVar=  ACCESS_TOKEN_ENV_VAR_NAME.format(accountIndStr)
    accessToken = os.environ.get(currAccessTokenEnvVar)
    assert accessToken != None, missingEnvVarErrorStr.format("API Access Token", accountIndStr)

    currAccessTokenSecretEnvVar = ACCESS_TOKEN_SECRET_ENV_VAR_NAME.format(accountIndStr)
    accessTokenSecret = os.environ.get(currAccessTokenSecretEnvVar)
    assert accessTokenSecret != None, missingEnvVarErrorStr.format("API Access Token Secret", accountIndStr)

    return apiKey, apiSecretKey, accessToken, accessTokenSecret
