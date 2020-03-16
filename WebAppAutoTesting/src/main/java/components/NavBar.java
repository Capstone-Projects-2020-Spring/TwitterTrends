package components;

import components.base.BaseAnalysisControlBar;
import components.base.BaseComponent;
import enums.AnalysisPages;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import pages.HomePage;
import pages.base.BaseAnalysisPage;

import java.util.List;

/**
 * POM representation of the navigation bar at the top of each page on the website
 */
public class NavBar extends BaseComponent
{
protected By siteLogoLoc = By.className("navbar-brand");
protected By analysisPageDropdownButtonLoc = By.id("pages-drop-btn");
protected By analysisPageDropdownOptionsContainerLoc = By.id("pages-dropdown-menu");
protected By analysisPageDropdownOption = By.tagName("a");

public NavBar( final WebDriver driver )
{
	super(driver);
}

public boolean isSiteLogoDisplayed( ) { return checkForDisplayedElement(siteLogoLoc); }

public boolean isDropdownEnabled( ) { return checkForEnabledElement(analysisPageDropdownButtonLoc); }

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
	
	WebElement navDropdown = getEnabledElement(analysisPageDropdownButtonLoc);
	clickElem(navDropdown);
	
	WebElement dropdownOptionsContainer = getElement(analysisPageDropdownOptionsContainerLoc);
	List<WebElement> dropdownOptions = getEnabledElements(analysisPageDropdownOption, dropdownOptionsContainer);
	
	String targetText = pageDesc.getDropdownOptionText();
	WebElement targetDropdownOption = null;
	for ( int i = 0 ; i < dropdownOptions.size() && targetDropdownOption == null ; i++ )
	{
		WebElement currOption = dropdownOptions.get(i);
		String optionText = getText(currOption);
		if ( targetText.equals(optionText) ) { targetDropdownOption = currOption; }
	}
	
	clickElem(targetDropdownOption);
	
	waitForPageLoad(targetDropdownOption);
	analysisPage = pageDesc.getPageInstance(driver);
	
	return analysisPage;
}

/**
 * clicks on the site logo to navigate back to the site's home page
 *
 * @return a POM representation of the site's home page
 */
public HomePage openHomePage( )
{
	WebElement logoElem = getElement(siteLogoLoc);
	clickElem(logoElem);
	waitForPageLoad(logoElem);
	HomePage homePage = new HomePage(driver);
	return homePage;
}
}
