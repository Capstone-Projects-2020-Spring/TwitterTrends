package api;

import api.base.BaseApiTest;
import api.responses.Trend;
import base.enums.Locations;
import io.restassured.response.Response;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.List;

import static io.restassured.RestAssured.given;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
 * automated tests of the /toptrends endpoint of the backend server's API
 */
public class TopTrendsApiTests extends BaseApiTest
{

protected static final String WOEID_ARG = "woeid";
protected static final String LAT_ARG1 = "latitude";
protected static final String LAT_ARG2 = "lat";
protected static final String LONG_ARG1 = "longitude";
protected static final String LONG_ARG2 = "long";
protected static final String NUM_ARG = "num";
protected static final String SORT_ARG = "sort";

@Override
protected String getEndpoint( ) { return "toptrends"; }

@Test
public void getTrendsWithWoeidHappyTest( )
{
	Response response = given().param(WOEID_ARG, Locations.BIRMINGHAM.getWoeidStr())
							   .get();
	List<Trend> trends = parseTrends(response);
	assertNotNull(trends);
	int numTrends = trends.size();
	Assertions.assertTrue(numTrends > 0);
}

@Test
public void getNumTrendsWithWoeidTest( )
{
	final int numTrends = 37;
	
	Response response = given().param(WOEID_ARG, Locations.SEATTLE.getWoeidStr())
							   .param(NUM_ARG, numTrends)
							   .get();
	List<Trend> trends = parseTrends(response);
	assertNotNull(trends);
	int fetchedTrendCount = trends.size();
	Assertions.assertEquals(numTrends, fetchedTrendCount);
}

@Test
public void getTrendsWithLatLongTest( )
{
	final double austinLatitude = 30.2672;
	final double austinLongitude = 97.7431;
	
	Response latLongResponse = given().param(LAT_ARG1, austinLatitude)
									  .param(LONG_ARG1, austinLongitude)
									  .get();
	Response woeidResponse = given().param(WOEID_ARG, Locations.AUSTIN.getWoeidStr())
									.get();
	
	List<Trend> latLongTrends = parseTrends(latLongResponse);
	List<Trend> woeidTrends = parseTrends(woeidResponse);
	
	assertNotNull(latLongTrends);
	assertNotNull(woeidTrends);
	//todo test that they share some elements, or test that they're the same?
	
}
}
