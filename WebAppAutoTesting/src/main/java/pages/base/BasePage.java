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

public U getNavBar( ) { return navBar; }

/**
 * checks whether the page which is currently loaded in the browser is the same one which is described by this
 * POM class
 *
 * @return whether the page which is currently loaded in the browser is the same one which is described by this
 * POM class
 */
public abstract boolean isCurrentPage( );
}
