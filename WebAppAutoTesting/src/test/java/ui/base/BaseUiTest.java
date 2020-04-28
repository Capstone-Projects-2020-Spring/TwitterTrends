package ui.base;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriverService;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.RemoteWebDriver;
import ui.pages.HomePage;

import java.io.File;
import java.io.IOException;
import java.nio.file.FileSystems;

/**
 * contains utilities for all automated tests of the website
 */
public class BaseUiTest
{
static final String RELATIVE_CHROME_DRIVER_PATH = "src/main/java/ui/chromedriver.exe";
static final String DOMAIN_NAME = "http://www.twittervisualtrends.com";

private static ChromeDriverService service;
protected WebDriver driver;

protected HomePage startPage;

@BeforeAll
public static void startTestSuite( ) throws IOException
{
	service = new ChromeDriverService.Builder().usingDriverExecutable(new File(getChromeDriverPath()))
											   .usingAnyFreePort()
											   .build();
	service.start();
}

	@AfterAll
	public static void cleanupTestSuite( )
	{
		try
		{
			//do other cleanup stuff
			service.stop();
		}
		catch ( Exception e ) { e.printStackTrace(); }
		finally { service.stop(); }
	}

	@BeforeEach
	public void setUpTestCase( )
	{
		ChromeOptions options = new ChromeOptions();
		options.addArguments("start-maximized");
		driver = new RemoteWebDriver(service.getUrl(), options);
		this.startPage = loadWebsite();
	}

	@AfterEach
	public void tearDownTestCase( )
	{
		try
		{
			this.startPage = null;
			//do other cleanup stuff
			driver.quit();
		}
		catch ( Exception e ) { e.printStackTrace(); }
		finally { driver.quit(); }
	}

protected HomePage loadWebsite( )
{
	driver.get(DOMAIN_NAME);
	HomePage startPage = new HomePage(driver);
	return startPage;
}

protected static String getChromeDriverPath( )
{
	String absoluteChromeDriverPath = FileSystems.getDefault()
												 .getPath(RELATIVE_CHROME_DRIVER_PATH)
												 .normalize()
												 .toAbsolutePath()
												 .toString();
	return absoluteChromeDriverPath;
}
}
