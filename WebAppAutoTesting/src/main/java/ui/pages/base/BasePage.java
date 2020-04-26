package ui.pages.base;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import ui.base.BasePageObject;
import ui.components.NavBar;

/**
 * POM representation of the elements in common among all ui.pages of the website
 */
public abstract class BasePage extends BasePageObject
{
protected By pageTitleLoc = By.id("title");

protected String pageTitle;

protected NavBar navBar;

protected BasePage( final WebDriver driver, final String titleText )
{
	super(driver);
	this.pageTitle = titleText;
}

public NavBar getNavBar( ) { return navBar; }

/**
 * checks whether the page which is currently loaded in the browser is the same one which is described by this
 * POM class
 *
 * @return whether the page which is currently loaded in the browser is the same one which is described by this
 * POM class
 */
public boolean isCurrentPage( )
{
	boolean isCurrPage = false;
	
	if ( checkForDisplayedElement(pageTitleLoc) )
	{
		WebElement titleElem = getDisplayedElement(pageTitleLoc);
		String titleText = getText(titleElem);
		if ( this.pageTitle.equals(titleText) ) { isCurrPage = true; }
	}
	
	return isCurrPage;
}
}
