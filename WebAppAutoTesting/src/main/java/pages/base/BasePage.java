package pages.base;

import base.BasePageObject;
import components.NavBar;
import org.openqa.selenium.WebDriver;

/**
 * POM representation of the elements in common among all pages of the website
 */
public abstract class BasePage extends BasePageObject
{
	protected NavBar navBar;

	protected BasePage( final WebDriver driver )
	{
		super(driver);
		this.navBar = new NavBar(driver);
	}

	//	TODO public abstract boolean isCurrentPage();

	public NavBar getNavBar( ) { return navBar; }
}
