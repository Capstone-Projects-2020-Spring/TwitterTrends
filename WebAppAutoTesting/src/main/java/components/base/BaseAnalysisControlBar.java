package components.base;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

/**
 * POM representation of elements common to the analysis control bars on all 'Analyze _' pages
 */
public abstract class BaseAnalysisControlBar extends BaseComponent
{
protected By searchFieldLoc = null;//todo
protected By updateGraphButtonLoc = null;//todo

protected BaseAnalysisControlBar( final WebDriver driver )
{
	super(driver);
}

/**
 * searches for analyses of something
 *
 * @param searchText description of the thing which should be searched for
 */
public void search( final String searchText )
{
	WebElement searchField = getEnabledElement(searchFieldLoc);
	enterText(searchField, searchText);
	//todo?
}

/**
 * refreshes the data visualization on the current analysis page
 */
public void updateGraph( ) { clickElem(updateGraphButtonLoc); }
}
