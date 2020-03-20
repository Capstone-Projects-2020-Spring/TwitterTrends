package pages;

import components.HomePageNavBar;
import components.TrendsDialog;
import enums.Locations;
import enums.States;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import pages.base.BasePage;

import java.util.Iterator;
import java.util.List;

/**
 * POM representation of the starting page of the website
 */
public class HomePage extends BasePage<HomePageNavBar>
{
protected TrendsDialog trendsDialog;

final protected By mapContainerLoc = By.id("svg");//todo make this less atrocious!!!
final protected By statesList = By.className("states");
final protected By stateEntry = By.tagName("path");
final protected String stateNameAttribute = "stateName";

final protected By locationsList = By.className("marker");
final protected By locationEntry = By.tagName("circle");
//final protected String locationNameAttribute = "cityName";
final protected String woeidAttribute = "woeid";

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
		List<WebElement> stateElems = getDisplayedElements(stateEntry, statesListElem);
		stateElems.removeIf(elem -> !elem.isDisplayed());
		stateCount = stateElems.size();
	}
	return stateCount;
}

public boolean isStateVisible( final States state )
{
	boolean stateVisible = false;
	WebElement stateElem = getState(state);
	if ( stateElem != null ) { stateVisible = checkIfDisplayed(stateElem); }
	return stateVisible;
}

public void clickState( final States state )
{
	WebElement stateElem = getState(state);
	clickElem(stateElem);
}

public TrendsDialog clickLocationMarker( final Locations loc )
{
	WebElement locElem = getLocationMarker(loc);
	clickElem(locElem);
	//todo should this be changed so the home page's dialog member changes when the dialog visibility changes?
	return this.trendsDialog;
}

public boolean isLocationMarkerVisible( final Locations loc )
{
	WebElement locElem = getLocationMarker(loc);
	return checkIfDisplayed(locElem);
}

protected WebElement getState( final States state )
{
	WebElement stateElem = null;
	String targetStateName = state.getStateName();
	
	WebElement mapContainerElem = getElement(mapContainerLoc);
	WebElement statesListContainer = getElement(statesList, mapContainerElem);
	List<WebElement> statesList = getElements(stateEntry, statesListContainer);
	
	Iterator<WebElement> stateIter = statesList.iterator();
	while ( stateIter.hasNext() && stateElem == null )
	{
		WebElement currState = stateIter.next();
		String currStateName = getAttribute(currState, stateNameAttribute);
		if ( targetStateName.equals(currStateName) ) { stateElem = currState; }
	}
	
	return stateElem;
}

protected WebElement getLocationMarker( final Locations loc )
{
	WebElement locMarkerElem = null;
	String targetLocWoeid = loc.getWoeidStr();
	
	WebElement mapContainerElem = getElement(mapContainerLoc);
	WebElement locationsListContainer = getElement(locationsList, mapContainerElem);
	List<WebElement> locationMarkersList = getElements(locationEntry, locationsListContainer);
	
	Iterator<WebElement> locationIter = locationMarkersList.iterator();
	while ( locationIter.hasNext() && locMarkerElem == null )
	{
		WebElement currLocation = locationIter.next();
		String currLocWoeid = getAttribute(currLocation, woeidAttribute);
		if ( targetLocWoeid.equals(currLocWoeid) ) { locMarkerElem = currLocation; }
	}
	
	return locMarkerElem;
}

@Override
public boolean isCurrentPage( ) { return navBar.isSearchBarEnabled(); }
}
