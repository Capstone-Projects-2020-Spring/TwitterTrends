package ui;

import org.junit.jupiter.api.Test;
import ui.base.BaseUiTest;
import ui.components.NavBar;
import ui.components.base.BaseAnalysisControlBar;
import ui.enums.AnalysisPages;
import ui.pages.HomePage;
import ui.pages.base.BaseAnalysisPage;
import ui.pages.base.BasePage;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * tests that major elements on each page of the website load and are displayed
 * (with interactive UI elements, the tests also check that those elements are 'probably' active/interactable)
 */
public class SiteLoadingTests extends BaseUiTest
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
	assertTrue(startPage.visibleLocationMarkerCount() > 0);
}

@Test
public void pagesNavigableTest( )
{
	NavBar navBar = startPage.getNavBar();
	assertTrue(navBar.isDropdownEnabled());
	assertTrue(navBar.isSiteLogoDisplayed());
	assertTrue(startPage.isCurrentPage());
	
	BasePage currPage = startPage;
	for ( AnalysisPages pageDesc : AnalysisPages.values() )
	{
		BaseAnalysisPage<? extends BaseAnalysisControlBar> analysisPage = currPage.getNavBar()
																				  .openAnalysisPage(pageDesc);
		NavBar analysisNavBar = analysisPage.getNavBar();
		assertTrue(analysisNavBar.isDropdownEnabled(), pageDesc.getDropdownOptionText());
		assertTrue(analysisNavBar.isSiteLogoDisplayed(), pageDesc.getDropdownOptionText());
		assertTrue(analysisPage.isCurrentPage(), pageDesc.getDropdownOptionText());
	}
	
	HomePage homePage = currPage.getNavBar()
								.openHomePage();
	NavBar homeNavBar = homePage.getNavBar();
	assertTrue(homeNavBar.isDropdownEnabled());
	assertTrue(homeNavBar.isSiteLogoDisplayed());
	assertTrue(homePage.isCurrentPage());
}
}
