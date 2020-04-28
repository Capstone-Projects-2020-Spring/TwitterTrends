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
protected List<Trend> parseTrends( final Response response )
{
	List<Trend> ret = null;
	
	String respJson = null;
	try
	{
		respJson = response.getBody()
						   .asString();
		
		Type returnType = new TypeToken<List<Trend>>() { }.getType();
		ret = gson.fromJson(respJson, returnType);
	} catch ( Exception e )
	{
		System.err.println("Couldn't parse a list of trends from a response." + "Response JSON string was: \n" +
						   ((respJson == null) ? "NULL :(" : respJson) + "\nException: " + e.getMessage());
	}
	
	return ret;
}

/**
 * converts the json of the response's body into a list of Tweet pojos
 *
 * @param response a response from the /toptweets endpoint
 *
 * @return a list of Tweets
 */
protected List<Tweet> parseTweets( final Response response )
{
	List<Tweet> ret = null;
	
	String respJson = null;
	try
	{
		respJson = response.getBody()
						   .asString();
		
		Type returnType = new TypeToken<List<Tweet>>() { }.getType();
		ret = gson.fromJson(respJson, returnType);
	} catch ( Exception e )
	{
		System.err.println("Couldn't parse a list of tweets from a response." + "Response JSON string was: \n" +
						   ((respJson == null) ? "NULL :(" : respJson) + "\nException: " + e.getMessage());
	}
	
	return ret;
}

/**
 * converts the json of the response's body into a Location pojo
 *
 * @param response a response from the /getlocation endpoint
 *
 * @return a location pojo
 */
protected Location parseLocation( final Response response )
{
	Location ret = null;
	
	String respJson = null;
	try
	{
		respJson = response.getBody()
						   .asString();
		
		Type returnType = new TypeToken<Location>() { }.getType();
		ret = gson.fromJson(respJson, returnType);
	} catch ( Exception e )
	{
		System.err.println("Couldn't parse a location from a response." + "Response JSON string was: \n" +
						   ((respJson == null) ? "NULL :(" : respJson) + "\nException: " + e.getMessage());
	}
	
	return ret;
}

/**
 * converts the json of the response's body into a list of Location pojos
 *
 * @param response a response from the /locations endpoint
 *
 * @return a list of location pojos
 */
protected List<Location> parseLocations( final Response response )
{
	List<Location> ret = null;
	
	String respJson = null;
	try
	{
		respJson = response.getBody()
						   .asString();
		
		Type returnType = new TypeToken<List<Location>>() { }.getType();
		ret = gson.fromJson(respJson, returnType);
	} catch ( Exception e )
	{
		System.err.println("Couldn't parse a list of locations from a response." + "Response JSON string was: \n" +
						   ((respJson == null) ? "NULL :(" : respJson) + "\nException: " + e.getMessage());
	}
	
	return ret;
}
}
