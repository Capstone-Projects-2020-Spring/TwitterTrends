package api.base;

import api.responses.Location;
import api.responses.Trend;
import api.responses.Tweet;
import com.google.gson.FieldNamingPolicy;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import io.restassured.RestAssured;
import io.restassured.response.Response;

import java.lang.reflect.Type;
import java.util.List;

/**
 * contains utilities for all automated tests of the backend server's API
 */
public abstract class BaseApiTest
{
protected Gson gson;

protected abstract String getEndpoint( );

public BaseApiTest( )
{
	RestAssured.baseURI = "http://18.214.197.203:5000/" + getEndpoint();
	gson = new GsonBuilder().setFieldNamingPolicy(FieldNamingPolicy.LOWER_CASE_WITH_UNDERSCORES)
							.create();
}

/**
 * converts the json of the response's body into a list of Trend pojos
 *
 * @param response a response from the /toptrends endpoint
 *
 * @return a list of Trends
 */
protected List<Trend> parseTrends( Response response )
{ return parseResponseJson(response, "a list of trends"); }

/**
 * converts the json of the response's body into a list of Tweet pojos
 *
 * @param response a response from the /toptweets endpoint
 *
 * @return a list of Tweets
 */
protected List<Tweet> parseTweets( Response response )
{ return parseResponseJson(response, "a list of tweets"); }

/**
 * converts the json of the response's body into a Location pojo
 *
 * @param response a response from the /getlocation endpoint
 *
 * @return a location pojo
 */
protected Location parseLocation( Response response )
{ return parseResponseJson(response, "a location"); }

/**
 * converts the json of the response's body into a list of Location pojos
 *
 * @param response a response from the /locations endpoint
 *
 * @return a list of location pojos
 */
protected List<Location> parseLocations( Response response )
{ return parseResponseJson(response, "a list of locations"); }

/**
 * parses the json of the response's body into some kind of pojo(s)
 *
 * @param response       a response from some api endpoint
 * @param retDescription a description of the pojo or pojos being parsed out of the json
 * @param <K>            the type of the object(s) being parsed out of the json
 *                       ie. this could be some collection type parameterized with some pojo class
 *
 * @return one or more pojos of some type
 */
private <K> K parseResponseJson( Response response, String retDescription )
{
	K ret = null;
	
	try
	{
		String respJson = response.getBody()
								  .asString();
		
		Type returnType = new TypeToken<K>() { }.getType();
		ret = gson.fromJson(respJson, returnType);
	} catch ( Exception e )
	{
		System.err.println("Couldn't parse " + retDescription + " from a response. Exception: " + e.getMessage());
	}
	
	return ret;
}
}
