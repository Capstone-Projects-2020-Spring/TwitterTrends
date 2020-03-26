package api.base;

import api.responses.Trend;
import api.responses.Tweet;
import com.google.gson.FieldNamingPolicy;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import io.restassured.RestAssured;
import io.restassured.response.Response;

import java.lang.reflect.Type;
import java.util.ArrayList;
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
 * @param resp a response from the /toptrends endpoint
 *
 * @return a list of Trends
 */
protected List<Trend> parseTrends( Response resp )
{
	List<Trend> trends = null;
	
	try
	{
		String respJson = resp.getBody()
							  .asString();
		
		Type trendListType = new TypeToken<ArrayList<Trend>>() { }.getType();
		trends = gson.fromJson(respJson, trendListType);
	} catch ( Exception e )
	{
		System.err.println("Couldn't parse trends from a response. Exception: " + e.getMessage());
	}
	
	return trends;
}

/**
 * converts the json of the response's body into a list of Tweet pojos
 *
 * @param resp a response from the /toptweets endpoint
 *
 * @return a list of Tweets
 */
protected List<Tweet> parseTweets( Response resp )
{
	List<Tweet> tweets = null;
	try
	{
		String respJson = resp.getBody()
							  .asString();
		
		Type trendListType = new TypeToken<ArrayList<Tweet>>() { }.getType();
		tweets = gson.fromJson(respJson, trendListType);
	} catch ( Exception e )
	{
		System.err.println("Couldn't parse tweets from a response. Exception: " + e.getMessage());
	}
	return tweets;
}
}
