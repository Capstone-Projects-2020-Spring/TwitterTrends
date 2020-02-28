package components;

import components.base.BaseAnalysisControlBar;
import components.base.BaseComponent;
import enums.AnalysisPages;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import pages.base.BaseAnalysisPage;

/**
 * POM representation of the navigation bar at the top of each page on the website
 */
public class NavBar extends BaseComponent
{
protected By siteTitleLoc = null;//todo
protected By analysisPageDropdownLoc = null;//todo

public NavBar( final WebDriver driver )
{
	super(driver);
}

public boolean isSiteTitleDisplayed( ) { return checkForDisplayedElement(siteTitleLoc); }

public boolean isDropdownEnabled( ) { return checkForEnabledElement(analysisPageDropdownLoc); }
//todo check whether dropdown can be expanded and whether the expected options are all there (see enum)

//todo click title to go to homepage?

/**
 * opens one of the analysis pages
 *
 * @param pageDesc description of the analysis page which will be navigated to
 * @param <T>      the class of the POM representation of the analysis page which will be navigated to
 *
 * @return a POM representation of the analysis page which will be navigated to
 */
public <T extends BaseAnalysisPage<? extends BaseAnalysisControlBar>> T openAnalysisPage( AnalysisPages pageDesc )
{
	T analysisPage = null;
	
	WebElement navDropdown = getEnabledElement(analysisPageDropdownLoc);
	//todo cast to Select?
	//todo expand element
	//todo find correct option element & click it
	
	analysisPage = pageDesc.getPageInstance(driver);
	
	return analysisPage;
}
}
