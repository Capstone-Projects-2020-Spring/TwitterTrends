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

final By mapContainerLoc = null;//todo!!!
final By statesList = By.className("states");
final By stateShapeDescription = By.tagName("path");
final By stateBorders = By.className("state-borders");

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

public boolean areStateBordersDisplayed( )
{
	boolean areBordersDisplayed = false;
	WebElement mapContainerElem = getDisplayedElement(mapContainerLoc);
	areBordersDisplayed = checkForElement(stateBorders, mapContainerElem);
	return areBordersDisplayed;
}
}
