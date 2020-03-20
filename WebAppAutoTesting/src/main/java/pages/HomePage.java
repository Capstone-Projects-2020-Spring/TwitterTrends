package pages;

import components.HomePageNavBar;
import components.TrendsDialog;
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
protected TrendsDialog trendsDialog;

final protected By mapContainerLoc = By.id("svg");//todo make this less atrocious!!!
final protected By statesList = By.className("states");
final protected By stateShapeDescription = By.tagName("path");

final protected By trendDetailsContainerLoc = null;//todo!!
//todo add locators for tweets section & news section of trend details

public HomePage( final WebDriver driver )
{
	super(driver);
	navBar = new HomePageNavBar(driver);
	this.trendsDialog = new TrendsDialog(driver);
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
