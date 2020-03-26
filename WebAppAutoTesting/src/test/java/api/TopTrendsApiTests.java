package api;

import api.base.BaseApiTest;

/**
 * automated tests of the /toptrends endpoint of the backend server's API
 */
public class TopTrendsApiTests extends BaseApiTest
{
@Override
protected String getEndpoint( ) { return "toptrends"; }
}
