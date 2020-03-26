package api;

import api.base.BaseApiTest;

/**
 * automated tests of the /locations endpoint of the backend server's API
 */
public class GetAllLocationsApiTest extends BaseApiTest
{

@Override
protected String getEndpoint( ) { return "locations"; }
}
