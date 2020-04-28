package ui.components.base;

import ui.base.BasePageObject;
import org.openqa.selenium.WebDriver;

/**
 * This contains anything that's common to all classes which represent a 'component' within a webpage as part of the POM
 */
public class BaseComponent extends BasePageObject
{

	protected BaseComponent( final WebDriver driver )
	{
		super(driver);
	}
}
