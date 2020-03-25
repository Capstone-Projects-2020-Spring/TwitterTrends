package ui;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import java.nio.file.FileSystems;

public class AutoTestProto
{

	@Test
	public void seleniumTest( )
	{
		String relativeChromeDriverPath = "src/main/chromedriver.exe";
		String absoluteChromeDriverPath = FileSystems.getDefault()
													 .getPath(relativeChromeDriverPath)
													 .normalize()
													 .toAbsolutePath()
													 .toString();
		System.setProperty("webdriver.chrome.driver", absoluteChromeDriverPath);

		WebDriver driver = new ChromeDriver();
		driver.get("http://www.google.com/");
		testPause();
		WebElement searchBox = driver.findElement(By.name("q"));
		searchBox.sendKeys("ChromeDriver");
		searchBox.submit();
		testPause();
		driver.quit();
	}

	private void testPause( )
	{
		try
		{
			Thread.sleep(3000);
		}
		catch ( InterruptedException e )
		{
			e.printStackTrace();
		}
	}
}
