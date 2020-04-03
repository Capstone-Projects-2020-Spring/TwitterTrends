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

@Test
public void getGreensboroByAddressTest( )
{
	Locations testLoc = Locations.GREENSBORO;
	Response response = given().param(ADDR_ARG, buildLocationAddrString(testLoc))
							   .get();
	Location location = parseLocation(response);
	validateLocation(location, testLoc);
}

@Test
public void getSaltLakeCityByAddressTest( )
{
	Locations testLoc = Locations.SALT_LAKE_CITY;
	Response response = given().param(ADDR_ARG, buildLocationAddrString(testLoc))
							   .get();
	Location location = parseLocation(response);
	validateLocation(location, testLoc);
}

@Test
public void getOmahaByAddressTest( )
{
	Locations testLoc = Locations.OMAHA;
	Response response = given().param(ADDR_ARG, buildLocationAddrString(testLoc))
							   .get();
	Location location = parseLocation(response);
	validateLocation(location, testLoc);
}

@Test
public void getRaleighByAddressTest( )
{
	Locations testLoc = Locations.RALEIGH;
	Response response = given().param(ADDR_ARG, buildLocationAddrString(testLoc))
							   .get();
	Location location = parseLocation(response);
	validateLocation(location, testLoc);
}

@Test
public void getNewYorkByAddressTest( )
{
	Locations testLoc = Locations.NEW_YORK;
	Response response = given().param(ADDR_ARG, buildLocationAddrString(testLoc))
							   .get();
	Location location = parseLocation(response);
	validateLocation(location, testLoc);
}

@Test
public void getSanFranciscoByAddressTest( )
{
	Locations testLoc = Locations.SAN_FRANCISCO;
	Response response = given().param(ADDR_ARG, buildLocationAddrString(testLoc))
							   .get();
	Location location = parseLocation(response);
	validateLocation(location, testLoc);
}

/**
 * verifies that a returned location pojo has expected values
 *
 * @param locPojo  the pojo parsed from an api response
 * @param location the enum entry describing what the location's values actually are
 */
public void validateLocation( Location locPojo, Locations location )
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
	if ( location != Locations.USA && location != Locations.WORLD )
	{ throw new IllegalArgumentException("can't build location address for a country or planet"); }
	
	String locAddr = location.getCityName() + ", " + location.getState()
															 .getStateName();
	return locAddr;
}
}
