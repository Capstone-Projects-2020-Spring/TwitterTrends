package ui;

import base.enums.Locations;
import base.enums.States;
import org.junit.jupiter.api.Test;
import ui.base.BaseUiTest;
import ui.components.TrendsDialog;
import ui.pages.HomePage;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
 * tests that some^ of the features of the map visualization on the home page are working
 *
 * ^specifically the ones which are amenable to automated testing
 */
public class MapVisualizationTests extends BaseUiTest
{

//todo try putting invalid location into search bar and assert that error message pops up

//todo try clicking on state then opening a location's trends inside that state
// e.g. colorado, michigan,

@Test
public void texasZoomTrendsLoadTest( )
{
	startPage.clickState(States.TEXAS);
	cityTrendsLoadTester(startPage, Locations.DALLAS);
}

@Test
public void rhodeIslandZoomTrendsLoadTest( )
{
	startPage.clickState(States.RHODE_ISLAND);
	cityTrendsLoadTester(startPage, Locations.PROVIDENCE);
}

@Test
public void floridaZoomTrendsLoadTest( )
{
	startPage.clickState(States.FLORIDA);
	cityTrendsLoadTester(startPage, Locations.ORLANDO);
}

@Test
public void californiaZoomTrendsLoadTest( )
{
	startPage.clickState(States.CALIFORNIA);
	cityTrendsLoadTester(startPage, Locations.SAN_DIEGO);
}

@Test
public void oregonZoomTrendsLoadTest( )
{
	startPage.clickState(States.OREGON);
	cityTrendsLoadTester(startPage, Locations.PORTLAND);
}

@Test
public void louisianaZoomTrendsLoadTest( )
{
	startPage.clickState(States.LOUISIANA);
	cityTrendsLoadTester(startPage, Locations.NEW_ORLEANS);
}

@Test
public void coloradoZoomTrendsLoadTest( )
{
	startPage.clickState(States.COLORADO);
	cityTrendsLoadTester(startPage, Locations.DENVER);
}

@Test
public void michiganZoomTrendsLoadTest( )
{
	startPage.clickState(States.MICHIGAN);
	cityTrendsLoadTester(startPage, Locations.DETROIT);
}

//hawaii zoom?

//todo try clicking on state, then clicking on state again, then investigating location far from that state

//todo verify that zoom excludes some of map by clicking on a state then investigating location far from that state
// how check whether something is cut off screen?

@Test
public void houstonTrendsLoadTest( )
{ cityTrendsLoadTester(startPage, Locations.HOUSTON); }

@Test
public void baltimoreTrendsLoadTest( )
{ cityTrendsLoadTester(startPage, Locations.BALTIMORE); }

@Test
public void seattleTrendsLoadTest( )
{ cityTrendsLoadTester(startPage, Locations.SEATTLE); }

@Test
public void indianapolisTrendsLoadTest( )
{ cityTrendsLoadTester(startPage, Locations.INDIANAPOLIS); }

@Test
public void orlandoTrendsLoadTest( )
{ cityTrendsLoadTester(startPage, Locations.ORLANDO); }

@Test
public void bostonTrendsLoadTest( )
{ cityTrendsLoadTester(startPage, Locations.BOSTON); }

@Test
public void houstonTrendDetailsLoadTest( )
{
	TrendsDialog trendsPopup = cityTrendsLoadTester(startPage, Locations.HOUSTON);
	List<String> houstonTrends = trendsPopup.getTopTrends();
	List<String> cleanedHoustonTrends = trendsPopup.cleanTrends(houstonTrends);
	trendsPopup.closeDialog();
	
	//todo after adding automation for right side of page
}

// todo click on a trend and verify that tweets with that trend showed up in the panel on the right

//todo open one location & check its trends then open another location & check that its trends are different?

@Test
public void tucsonAtlantaDifferentTrendsTest( )
{ citiesTrendsDifferentTester(startPage, Locations.TUCSON, Locations.ATLANTA); }

@Test
public void philadelphiaLADifferentTrendsTest( )
{ citiesTrendsDifferentTester(startPage, Locations.PHILADELPHIA, Locations.LOS_ANGELES); }

@Test
public void detroitMemphisDifferentTrendsTest( )
{ citiesTrendsDifferentTester(startPage, Locations.DETROIT, Locations.MEMPHIS); }

/**
 * helper function which verifies that two cities have different trends
 *
 * @param mapPage the page which the map visualization is on
 * @param city1   the first city whose top trends should be considered
 * @param city2   the second city whose top trends should be considered
 */
protected void citiesTrendsDifferentTester( final HomePage mapPage, final Locations city1, final Locations city2 )
{
	TrendsDialog firstCityTrendsPopup = cityTrendsLoadTester(mapPage, city1);
	List<String> firstCityTrends = firstCityTrendsPopup.getTopTrends();
	List<String> cleanedFirstCityTrends = firstCityTrendsPopup.cleanTrends(firstCityTrends);
	firstCityTrendsPopup.closeDialog();
	
	TrendsDialog secondCityTrendsPopup = cityTrendsLoadTester(mapPage, city2);
	List<String> secondCityTrends = secondCityTrendsPopup.getTopTrends();
	List<String> cleanedSecondCityTrends = secondCityTrendsPopup.cleanTrends(secondCityTrends);
	secondCityTrendsPopup.closeDialog();
	
	assertNotEquals(cleanedFirstCityTrends, cleanedSecondCityTrends);
}

/**
 * helper function which opens a given location's top trends dialog and verifies that trends for that city load
 *
 * @param mapPage the page which the map visualization is on
 * @param city    which city's top trends to check for
 *
 * @return the top trends dialog for the given location
 */
protected TrendsDialog cityTrendsLoadTester( final HomePage mapPage, final Locations city )
{
	TrendsDialog trendsPopup = mapPage.clickLocationMarker(city);
	trendsPopup.waitForTrendsLoaded();
	List<String> cityTrends = trendsPopup.getTopTrends();
	List<String> cleanedCityTrends = trendsPopup.cleanTrends(cityTrends);
	assertNotNull(cleanedCityTrends);
	System.out.println(cleanedCityTrends);
	return trendsPopup;
}
}
