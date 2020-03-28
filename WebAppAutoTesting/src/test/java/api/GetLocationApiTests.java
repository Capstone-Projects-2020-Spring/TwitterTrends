package api;

import api.base.BaseApiTest;

/**
 * automated tests of the /getlocation endpoint of the backend server's API
 */
public class GetLocationApiTests extends BaseApiTest
{

@Override
protected String getEndpoint( ) { return "getlocation"; }

protected static final String WOEID_ARG = "woeid";
protected static final String LAT_ARG1 = "latitude";
protected static final String LAT_ARG2 = "lat";
protected static final String LONG_ARG1 = "longitude";
protected static final String LONG_ARG2 = "long";
protected static final String ADDR_ARG = "address";
}
