import java.nio.file.FileSystems;

public class AutoTestProto
{

	public void seleniumTest( )
	{
		String relativeChromeDriverPath = "/src/main/chromedriver.exe";
		String absoluteChromeDriverPath = FileSystems.getDefault()
													 .getPath(relativeChromeDriverPath)
													 .normalize()
													 .toAbsolutePath()
													 .toString();
		System.setProperty("webdriver.chrome.driver", absoluteChromeDriverPath);
	}
}
