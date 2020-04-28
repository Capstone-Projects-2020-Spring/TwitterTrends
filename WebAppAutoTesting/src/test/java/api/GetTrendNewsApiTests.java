package api;

import api.base.BaseApiTest;

/**
 * automated tests of the /trend_news endpoint of the backend server's API
 */
public class GetTrendNewsApiTests extends BaseApiTest
{

@Override
protected String getEndpoint( ) { return "trend_news"; }
}
