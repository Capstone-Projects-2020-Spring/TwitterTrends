package ui;

import base.enums.Locations;
import base.enums.States;
import org.junit.jupiter.api.Test;
import ui.base.BaseUiTest;
import ui.components.TrendsDialog;
import ui.pages.HomePage;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

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
	assertFalse(startPage.isStateVisible(States.NORTH_DAKOTA));
	cityTrendsLoadTester(startPage, Locations.DALLAS);
}

@Test
public void rhodeIslandZoomTrendsLoadTest( )
{
	startPage.clickState(States.RHODE_ISLAND);
	assertFalse(startPage.isStateVisible(States.ARIZONA));
	cityTrendsLoadTester(startPage, Locations.PROVIDENCE);
}

@Test
public void marylandZoomUnzoomTrendsLoadTest( )
{
	startPage.clickState(States.MARYLAND);
	assertFalse(startPage.isStateVisible(States.NEBRASKA));
	startPage.clickState(States.MARYLAND);
	assertTrue(startPage.isStateVisible(States.NEBRASKA));
	cityTrendsLoadTester(startPage, Locations.BALTIMORE);
}

@Test
public void floridaZoomTrendsLoadTest( )
{
	startPage.clickState(States.FLORIDA);
	assertFalse(startPage.isStateVisible(States.IDAHO));
	cityTrendsLoadTester(startPage, Locations.ORLANDO);
}

@Test
public void californiaZoomTrendsLoadTest( )
{
	startPage.clickState(States.CALIFORNIA);
	assertFalse(startPage.isStateVisible(States.VERMONT));
	cityTrendsLoadTester(startPage, Locations.SAN_DIEGO);
}

@Test
public void oregonZoomUnzoomTrendsLoadTest( )
{
	startPage.clickState(States.OREGON);
	assertFalse(startPage.isStateVisible(States.SOUTH_CAROLINA));
	startPage.clickState(States.OREGON);
	assertTrue(startPage.isStateVisible(States.SOUTH_CAROLINA));
	cityTrendsLoadTester(startPage, Locations.PORTLAND);
}

@Test
public void louisianaZoomTrendsLoadTest( )
{
	startPage.clickState(States.LOUISIANA);
	assertFalse(startPage.isStateVisible(States.MAINE));
	cityTrendsLoadTester(startPage, Locations.NEW_ORLEANS);
}

@Test
public void connecticutZoomTrendsLoadTest( )
{
	startPage.clickState(States.CONNECTICUT);
	assertFalse(startPage.isStateVisible(States.NEVADA));
	cityTrendsLoadTester(startPage, Locations.NEW_HAVEN);
}

@Test
public void virginiaZoomUnzoomTrendsLoadTest( )
{
	startPage.clickState(States.VIRGINIA);
	assertFalse(startPage.isStateVisible(States.IDAHO));
	startPage.clickState(States.VIRGINIA);
	assertTrue(startPage.isStateVisible(States.IDAHO));
	cityTrendsLoadTester(startPage, Locations.RICHMOND);
}

@Test
public void coloradoZoomTrendsLoadTest( )
{
	startPage.clickState(States.COLORADO);
	assertFalse(startPage.isStateVisible(States.GEORGIA));
	cityTrendsLoadTester(startPage, Locations.DENVER);
}

@Test
public void michiganZoomUnzoomTrendsLoadTest( )
{
	startPage.clickState(States.MICHIGAN);
	assertFalse(startPage.isStateVisible(States.NEW_MEXICO));
	startPage.clickState(States.MICHIGAN);
	assertTrue(startPage.isStateVisible(States.NEW_MEXICO));
	cityTrendsLoadTester(startPage, Locations.DETROIT);
}

@Test
public void hawaiiZoomUnzoomTrendsLoadTest( )
{
	startPage.clickState(States.HAWAII);
	assertFalse(startPage.isStateVisible(States.WISCONSIN));
	startPage.clickState(States.HAWAII);
	assertTrue(startPage.isStateVisible(States.WISCONSIN));
	cityTrendsLoadTester(startPage, Locations.HONOLULU);
}

@Test
public void kentuckyZoomTrendsLoadTest( )
{
	startPage.clickState(States.KENTUCKY);
	assertFalse(startPage.isStateVisible(States.OREGON));
	cityTrendsLoadTester(startPage, Locations.LOUISVILLE);
}

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
	trendsPopup.closeDialog();
	
	//todo after adding automation for right side of page
}

// todo click on a trend and verify that tweets with that trend showed up in the panel on the right

//todo open one location & check its trends then open another location & check that its trends are different?

@Test
public void tucsonAtlantaDifferentTrendsTest( )
{ citiesTrendsDifferentTester(startPage, Locations.TUCSON, Locations.ATLANTA); }

@Test
public void philadelphiaMinneapolisDifferentTrendsTest( )
{ citiesTrendsDifferentTester(startPage, Locations.PHILADELPHIA, Locations.MINNEAPOLIS); }

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
	firstCityTrendsPopup.closeDialog();
	
	TrendsDialog secondCityTrendsPopup = cityTrendsLoadTester(mapPage, city2);
	List<String> secondCityTrends = secondCityTrendsPopup.getTopTrends();
	secondCityTrendsPopup.closeDialog();
	
	assertNotEquals(firstCityTrends, secondCityTrends);
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
	assertNotNull(cityTrends);
	System.out.println(cityTrends);
	return trendsPopup;
}
}
