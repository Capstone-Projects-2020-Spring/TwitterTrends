package base;

import org.openqa.selenium.WebDriver;

/**
 * this contains utility functions needed by most or all classes which represent entities on the website (based on the
 * Page Object Model (POM))
 */
public class BasePageObject
{
	protected WebDriver driver;

	//todo implement waitForElementPresent/Displayed/Enabled functions
	// custom ExpectedCondition!

	//TODO replicate waitForPageLoad() functionality
	// jquery, angular, documentState checks? running javascript to check those statuses
	// small amounts of use of thread.sleep
	// Maybe can be simpler, because limited to a single website!?!
}
