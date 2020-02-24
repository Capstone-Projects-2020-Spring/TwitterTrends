package base;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriverService;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.RemoteWebDriver;

import java.io.File;
import java.io.IOException;
import java.nio.file.FileSystems;

/**
 * contains utilities for all automated tests of the website
 */
public class BaseTest
{
	static final String RELATIVE_CHROME_DRIVER_PATH = "src/main/chromedriver.exe";

	private static ChromeDriverService service;
	protected WebDriver driver;

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
		driver = new RemoteWebDriver(service.getUrl(), new ChromeOptions());
	}

	@AfterEach
	public void tearDownTestCase( )
	{
		try
		{
			//do other cleanup stuff
			driver.quit();
		}
		catch ( Exception e ) { e.printStackTrace(); }
		finally { driver.quit(); }
	}

	//todo have @BeforeAll func set up ChromeDriverService

	//todo have @BeforeEach func set up RemoteWebDriver?

	//todo have @AfterEach func quit the WebDriver

	//todo have @AfterAll func break down ChromeDriverService

	//todo implement

	//TODO replicate waitForPageLoad() functionality
	// jquery, angular, documentState checks? running javascript to check those statuses
	// small amounts of use of thread.sleep
	// Maybe can be simpler, because limited to a single website!?!

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
