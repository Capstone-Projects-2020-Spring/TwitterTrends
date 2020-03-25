package ui.pages.base;

import ui.components.NavBar;
import ui.components.base.BaseAnalysisControlBar;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

/**
 * POM representation of shared ui.components among 'Analyze _' ui.pages on the website
 */
public abstract class BaseAnalysisPage<T extends BaseAnalysisControlBar> extends BasePage<NavBar>
{
protected By pageTitleLoc = By.id("title");

protected T controlBar;
protected String pageTitle;

protected BaseAnalysisPage( final WebDriver driver, final String titleText )
{
	super(driver);
	this.navBar = new NavBar(driver);
	this.pageTitle = titleText;
}

public T getControlBar( ) { return controlBar; }

@Override
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
