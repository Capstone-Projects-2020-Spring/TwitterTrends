package api.base;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeAll;

/**
 * contains utilities for all automated tests of the backend server's API
 */
public abstract class BaseApiTest
{
protected abstract String getEndpoint( );

@BeforeAll
public static void setUpTest( )
{
	RestAssured.baseURI = "http://18.214.197.203:5000/";
}
}
