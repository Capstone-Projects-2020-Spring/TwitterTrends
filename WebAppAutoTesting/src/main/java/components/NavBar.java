package components;

import components.base.BaseComponent;
import org.openqa.selenium.WebDriver;

/**
 * POM representation of the navigation bar at the top of each page on the website
 */
public class NavBar extends BaseComponent
{

	public NavBar( final WebDriver driver )
	{
		super(driver);
	}
}
