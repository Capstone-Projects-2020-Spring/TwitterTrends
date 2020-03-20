import base.BaseTest;
import components.HomePageNavBar;
import components.NavBar;
import components.base.BaseAnalysisControlBar;
import enums.AnalysisPages;
import org.junit.jupiter.api.Test;
import pages.HomePage;
import pages.base.BaseAnalysisPage;
import pages.base.BasePage;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * tests that major elements on each page of the website load and are displayed
 * (with interactive UI elements, the tests also check that those elements are 'probably' active/interactable)
 */
public class SiteLoadingTests extends BaseTest
{
protected final int expectedNumStates = 51;

@Test
public void siteLoadsTest( )
{
	NavBar navBar = startPage.getNavBar();
	assertTrue(navBar.isSiteLogoDisplayed());
	assertTrue(navBar.isDropdownEnabled());
}

@Test
public void mapLoadsTest( )
{
	assertEquals(expectedNumStates, startPage.visibleStateCount());
	//todo also check for existence of some location markers
}

@Test
public void pagesNavigableTest( )
{
	HomePageNavBar navBar = startPage.getNavBar();
	assertTrue(navBar.isDropdownEnabled());
	assertTrue(navBar.isSiteLogoDisplayed());
	assertTrue(navBar.isSearchBarEnabled());
	assertTrue(startPage.isCurrentPage());
	
	BasePage<HomePageNavBar> currPage = startPage;
	for ( AnalysisPages pageDesc : AnalysisPages.values() )
	{
		BaseAnalysisPage<? extends BaseAnalysisControlBar> analysisPage = currPage.getNavBar()
																				  .openAnalysisPage(pageDesc);
		NavBar analysisNavBar = analysisPage.getNavBar();
		assertTrue(analysisNavBar.isDropdownEnabled());
		assertTrue(analysisNavBar.isSiteLogoDisplayed());
		assertTrue(analysisPage.isCurrentPage());
	}
	
	HomePage homePage = currPage.getNavBar()
								.openHomePage();
	HomePageNavBar homeNavBar = homePage.getNavBar();
	assertTrue(homeNavBar.isDropdownEnabled());
	assertTrue(homeNavBar.isSiteLogoDisplayed());
	assertTrue(homeNavBar.isSearchBarEnabled());
	assertTrue(homePage.isCurrentPage());
}
}