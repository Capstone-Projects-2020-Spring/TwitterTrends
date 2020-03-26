package api;

import api.base.BaseApiTest;

/**
 * automated tests of the /getlocation endpoint of the backend server's API
 */
public class GetLocationApiTests extends BaseApiTest
{

@Override
protected String getEndpoint( ) { return "getlocation"; }
}
