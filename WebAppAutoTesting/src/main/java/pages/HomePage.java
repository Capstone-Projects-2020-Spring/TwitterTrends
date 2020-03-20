package pages;

import components.HomePageNavBar;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import pages.base.BasePage;

import java.util.ArrayList;
import java.util.List;

/**
 * POM representation of the starting page of the website
 */
public class HomePage extends BasePage<HomePageNavBar>
{

final By mapContainerLoc = By.id("svg");//todo make this less atrocious!!!
final By statesList = By.className("states");
final By stateShapeDescription = By.tagName("path");

final By trendPopupContainerLoc = By.id("bg-modal");
final By trendPopupTitle = By.className("top-trends-title");
final By trendPopupTrendsList = By.className("top-trends-ul");
final By trendPopupEntry = By.tagName("li");
final String trendPopupEntryTemplate = "[1-5]\\. .+";

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

public List<String> getTopTrends( )
{
	List<String> trends = new ArrayList<>();
	
	WebElement popupContainer = getElement(trendPopupContainerLoc);
	//waits for contents of popup to be displayed
	getDisplayedElement(trendPopupTitle, popupContainer);
	WebElement trendsListContainer = getElement(trendPopupTrendsList, popupContainer);
	
	List<WebElement> trendElems = getDisplayedElements(trendPopupEntry, trendsListContainer);
	for ( WebElement elem : trendElems )
	{
		String elemText = getText(elem);
		if ( elemText.matches(trendPopupEntryTemplate) )
		{
			//cut out the starting template with the entry index
			elemText = elemText.substring(3);
			trends.add(elemText);
		}
		else { trends.add(null); }
	}
	return trends;
}

public boolean isTrendPopupDisplayed( )
{
	WebElement popupContainer = getElement(trendPopupContainerLoc);
	return checkForDisplayedElement(trendPopupTitle, popupContainer);
}

@Override
public boolean isCurrentPage( ) { return navBar.isSearchBarEnabled(); }

protected By getPopupTrendEntryLoc( final int entryIndex )
{
	if ( entryIndex < 1 || entryIndex > 5 )
	{
		throw new IllegalArgumentException("there is never a trend entry with index " + entryIndex);
	}
	String trendEntryClass = String.format("trend-%d", entryIndex);
	By trendEntryLoc = By.className(trendEntryClass);
	return trendEntryLoc;
}
}
