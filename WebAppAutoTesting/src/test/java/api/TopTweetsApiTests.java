package api;

import api.base.BaseApiTest;

/**
 * automated tests of the /toptweets endpoint of the backend server's API
 */
public class TopTweetsApiTests extends BaseApiTest
{

@Override
protected String getEndpoint( ) { return "toptweets"; }
}
