package pages.base;

import base.BasePageObject;
import components.NavBar;

/**
 * POM representation of the elements in common among all pages of the website
 */
public abstract class BasePage extends BasePageObject
{
	protected NavBar navBar;

	protected BasePage( )
	{
		this.navBar = new NavBar();
	}

	//	TODO public abstract boolean isCurrentPage();

	public NavBar getNavBar( ) { return navBar; }
}
