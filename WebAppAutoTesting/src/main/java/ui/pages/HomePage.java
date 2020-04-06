package ui.pages;

import base.enums.Locations;
import base.enums.States;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import ui.components.HomePageNavBar;
import ui.components.TrendsDialog;
import ui.pages.base.BasePage;

import java.util.List;

/**
 * POM representation of the starting page of the website
 */
public class HomePage extends BasePage<HomePageNavBar>
{
protected TrendsDialog trendsDialog;

final protected By mapContainerLoc = By.id("mapsvg");
final protected By statesList = By.className("states");
final protected By stateEntry = By.tagName("path");
final protected String stateNameAttribute = "state-name";

final protected By locationsList = By.className("marker");
final protected By locationEntry = By.tagName("circle");
final protected String locationNameAttribute = "city-name";
final protected String woeidAttribute = "woeid";

final protected By trendDetailsContainerLoc = null;//todo!!
//todo add locators for tweets section & news section of trend details

final protected static int MILLIS_WAIT_FOR_ZOOM_TRANSITION = 1250;

public HomePage( final WebDriver driver )
{
	super(driver);
	navBar = new HomePageNavBar(driver);
	this.trendsDialog = new TrendsDialog(driver);
}

/**
 * counts how many distinct states are displayed in the map
 *
 * @return how many distinct states are displayed in the map
 */
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

/**
 * counts how many location markers are displayed in the map
 *
 * @return how many location markers are displayed in the map
 */
public int visibleLocationMarkerCount( )
{
	int locMarkerCount = -1;
	WebElement mapContainerElem = getElement(mapContainerLoc);
	if ( checkForElement(locationsList) )
	{
		WebElement locationsListElem = getElement(locationsList, mapContainerElem);
		List<WebElement> locationMarkerElems = getDisplayedElements(locationEntry, locationsListElem);
		locationMarkerElems.removeIf(elem -> !elem.isDisplayed());
		locMarkerCount = locationMarkerElems.size();
	}
	return locMarkerCount;
}

/**
 * determines whether a state is or shortly becomes visible
 *
 * @param state the state which should be/become visible
 *
 * @return whether a state is or shortly becomes visible
 */
public boolean isStateVisible( final States state )
{
	boolean stateVisible = false;
	WebElement stateElem = getState(state);
	if ( stateElem != null ) { stateVisible = checkIfDisplayed(stateElem); }
	return stateVisible;
}

/**
 * clicks on a given state's element in the map
 * @param state which state to click on
 */
public void clickState( final States state )
{
	WebElement stateElem = getState(state);
	clickElemWithOffset(stateElem, state.getHorizOffsetFraction(), state.getVertOffsetFraction());
	sleep(MILLIS_WAIT_FOR_ZOOM_TRANSITION);
}

/**
 * clicks on a particular location's marker on the map
 * @param loc which location to click on
 * @return the top trends dialog for that location
 */
public TrendsDialog clickLocationMarker( final Locations loc )
{
	WebElement locElem = getLocationMarker(loc);
	clickElem(locElem);
	//todo should this be changed so the home page's dialog member changes when the dialog visibility changes?
	return this.trendsDialog;
}

/**
 * determines whether a location's marker is or shortly becomes visible
 * @param loc the location which should be/become visible
 * @return whether a location's marker is or shortly becomes visible
 */
public boolean isLocationMarkerVisible( final Locations loc )
{
	WebElement locElem = getLocationMarker(loc);
	return checkIfDisplayed(locElem);
}

/**
 * finds the element for a given state
 * @param state which state's element should be retrieved
 * @return the element for a given state
 */
protected WebElement getState( final States state )
{
	WebElement stateElem = null;
	String targetStateName = state.getStateName();
	
	WebElement mapContainerElem = getElement(mapContainerLoc);
	WebElement statesListContainer = getElement(statesList, mapContainerElem);
	List<WebElement> statesList = getElements(stateEntry, statesListContainer);
	
	for ( WebElement currState : statesList )
	{
		String currStateName = getAttribute(currState, stateNameAttribute);
		if ( targetStateName.equals(currStateName) )
		{
			stateElem = currState;
			break;
		}
	}
	
	return stateElem;
}

/**
 * finds the marker for a given location
 * @param loc which location's marker should be found
 * @return the marker for a given location
 */
protected WebElement getLocationMarker( final Locations loc )
{
	WebElement locMarkerElem = null;
	String targetLocWoeid = loc.getWoeidStr();
	
	WebElement mapContainerElem = getElement(mapContainerLoc);
	WebElement locationsListContainer = getElement(locationsList, mapContainerElem);
	List<WebElement> locationMarkersList = getElements(locationEntry, locationsListContainer);
	
	for ( WebElement currLocation : locationMarkersList )
	{
		String currLocWoeid = getAttribute(currLocation, woeidAttribute);
		if ( targetLocWoeid.equals(currLocWoeid) )
		{
			locMarkerElem = currLocation;
			break;
		}
	}
	
	return locMarkerElem;
}

@Override
public boolean isCurrentPage( ) { return navBar.isSearchBarEnabled(); }
}
