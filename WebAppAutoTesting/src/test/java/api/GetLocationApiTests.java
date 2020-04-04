package api;

import api.base.BaseApiTest;
import api.responses.Location;
import base.enums.Locations;
import io.restassured.response.Response;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
 * automated tests of the /getlocation endpoint of the backend server's API
 */
public class GetLocationApiTests extends BaseApiTest
{

protected static final String WOEID_ARG = "woeid";
protected static final String LAT_ARG1 = "latitude";
protected static final String LAT_ARG2 = "lat";
protected static final String LONG_ARG1 = "longitude";
protected static final String LONG_ARG2 = "long";
protected static final String ADDR_ARG = "address";

protected static final double LAT_LONG_COMPARISON_THRESHOLD = 0.5;

@Override
protected String getEndpoint( ) { return "getlocation"; }

//HAPPY PATH TESTS

@Test
public void getGreensboroByAddressTest( ) { testLocByAddr(Locations.GREENSBORO); }

@Test
public void getSaltLakeCityByAddressTest( ) { testLocByAddr(Locations.SALT_LAKE_CITY); }

@Test
public void getOmahaByAddressTest( ) { testLocByAddr(Locations.OMAHA); }

@Test
public void getRaleighByAddressTest( ) { testLocByAddr(Locations.RALEIGH); }

@Test
public void getNewYorkByAddressTest( ) { testLocByAddr(Locations.NEW_YORK); }

@Test
public void getSanFranciscoByAddressTest( ) { testLocByAddr(Locations.SAN_FRANCISCO); }

@Test
public void getGreensboroByWoeidTest( ) { testLocByWoeid(Locations.GREENSBORO); }

@Test
public void getSaltLakeCityByWoeidTest( ) { testLocByWoeid(Locations.SALT_LAKE_CITY); }

@Test
public void getOmahaByWoeidTest( ) { testLocByWoeid(Locations.OMAHA); }

@Test
public void getRaleighByWoeidTest( ) { testLocByWoeid(Locations.RALEIGH); }

@Test
public void getNewYorkByWoeidTest( ) { testLocByWoeid(Locations.NEW_YORK); }

@Test
public void getSanFranciscoByWoeidTest( ) { testLocByWoeid(Locations.SAN_FRANCISCO); }

@Test
public void getGreensboroByLatLongTest( ) { testLocByLatLong(Locations.GREENSBORO); }

@Test
public void getSaltLakeCityByLatLongTest( ) { testLocByLatLong(Locations.SALT_LAKE_CITY); }

@Test
public void getOmahaByLatLongTest( ) { testLocByLatLong(Locations.OMAHA); }

@Test
public void getRaleighByLatLongTest( ) { testLocByLatLong(Locations.RALEIGH); }

@Test
public void getNewYorkByLatLongTest( ) { testLocByLatLong(Locations.NEW_YORK); }

@Test
public void getSanFranciscoByLatLongTest( ) { testLocByLatLong(Locations.SAN_FRANCISCO); }

//NEGATIVE TESTS todo

// TEST HELPER FUNCTIONS

/**
 * tests the api endpoint for a particular location by sending a vague address string for the city
 *
 * @param testLoc the location to be tested
 */
protected void testLocByAddr( Locations testLoc )
{
	Response response = given().param(ADDR_ARG, buildLocationAddrString(testLoc))
							   .get();
	Location location = parseLocation(response);
	validateLocation(location, testLoc);
}

/**
 * tests the api endpoint for a particular location by sending the city's woeid
 *
 * @param testLoc the location to be tested
 */
protected void testLocByWoeid( Locations testLoc )
{
	Response response = given().param(WOEID_ARG, testLoc.getWoeidStr())
							   .get();
	Location location = parseLocation(response);
	validateLocation(location, testLoc);
}

/**
 * tests the api endpoint for a particular location by sending the city's latitude and longitude
 *
 * tests both ways of sending either parameter to the endpoint
 *
 * @param testLoc the location to be tested
 */
protected void testLocByLatLong( Locations testLoc )
{
	//full names - latitude & longitude
	Response response = given().param(LAT_ARG1, testLoc.getLatitude())
							   .param(LONG_ARG1, testLoc.getLongitude())
							   .get();
	Location location = parseLocation(response);
	validateLocation(location, testLoc);
	
	//full and short names - latitude & long
	response = given().param(LAT_ARG1, testLoc.getLatitude())
					  .param(LONG_ARG2, testLoc.getLongitude())
					  .get();
	location = parseLocation(response);
	validateLocation(location, testLoc);
	
	//short full names - lat & longitude
	response = given().param(LAT_ARG2, testLoc.getLatitude())
					  .param(LONG_ARG1, testLoc.getLongitude())
					  .get();
	location = parseLocation(response);
	validateLocation(location, testLoc);
	
	//short names - lat & long
	response = given().param(LAT_ARG2, testLoc.getLatitude())
					  .param(LONG_ARG2, testLoc.getLongitude())
					  .get();
	location = parseLocation(response);
	validateLocation(location, testLoc);
}

/**
 * verifies that a returned location pojo has expected values
 *
 * @param locPojo  the pojo parsed from an api response
 * @param location the enum entry describing what the location's values actually are
 */
protected void validateLocation( Location locPojo, Locations location )
{
	assertNotNull(locPojo);
	assertEquals(location.getCityName(), locPojo.getCityId());
	assertEquals(location.getWoeidVal(), locPojo.getWoeid());
	assertEquals(location.getLatitude(), locPojo.getLatitude(), LAT_LONG_COMPARISON_THRESHOLD);
	assertEquals(location.getLongitude(), locPojo.getLongitude(), LAT_LONG_COMPARISON_THRESHOLD);
}

/**
 * creates a string for the 'address' of a city
 *
 * @param location which location to make the address of
 *
 * @return a string containing a minimal address for the location
 */
protected String buildLocationAddrString( Locations location )
{
	if ( location == Locations.USA || location == Locations.WORLD )
	{ throw new IllegalArgumentException("can't build location address for a country or planet"); }
	
	String locAddr = location.getCityName() + ", " + location.getState()
															 .getStateName();
	return locAddr;
}
}
