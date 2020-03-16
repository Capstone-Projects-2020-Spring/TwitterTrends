package pages;

import components.HomePageNavBar;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import pages.base.BasePage;

import java.util.List;

/**
 * POM representation of the starting page of the website
 */
public class HomePage extends BasePage<HomePageNavBar>
{

final By mapContainerLoc = By.tagName("svg");//todo make this less atrocious!!!
final By statesList = By.className("states");
final By stateShapeDescription = By.tagName("path");

final By trendDetailsContainerLoc = null;//todo!!
//todo add locators for tweets section & news section of trend details

public HomePage( final WebDriver driver )
{
	super(driver);
	navBar = new HomePageNavBar(driver);
}

public int visibleStateCount( )
{
	int stateCount = -1;
	WebElement mapContainerElem = getElement(mapContainerLoc);
	if ( checkForElement(statesList) )
	{
		WebElement statesListElem = getElement(statesList, mapContainerElem);
		List<WebElement> stateElems = getDisplayedElements(stateShapeDescription, statesListElem);
		stateElems.removeIf(elem -> !elem.isDisplayed());
		stateCount = stateElems.size();
	}
	return stateCount;
}

@Override
public boolean isCurrentPage( ) { return navBar.isSearchBarEnabled(); }
}
