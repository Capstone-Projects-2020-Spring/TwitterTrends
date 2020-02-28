package pages.base;

import base.BasePageObject;
import components.NavBar;
import org.openqa.selenium.WebDriver;

/**
 * POM representation of the elements in common among all pages of the website
 */
public abstract class BasePage<U extends NavBar> extends BasePageObject
{
protected U navBar;

protected BasePage( final WebDriver driver )
{
	super(driver);
}

//	TODO public abstract boolean isCurrentPage();

public U getNavBar( ) { return navBar; }
}
