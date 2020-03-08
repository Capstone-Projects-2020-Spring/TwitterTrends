import base.BaseTest;
import components.NavBar;
import org.junit.jupiter.api.Test;

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
	assertTrue(navBar.isSiteTitleDisplayed());
	assertTrue(navBar.isDropdownEnabled());
}

@Test
public void mapLoadsTest( )
{
	assertTrue(startPage.areStateBordersDisplayed());
	assertEquals(expectedNumStates, startPage.visibleStateCount());
}
}
