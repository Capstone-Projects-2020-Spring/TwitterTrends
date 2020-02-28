import base.BaseTest;
import components.NavBar;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * tests that major elements on each page of the website load and are displayed
 * (with interactive UI elements, the tests also check that those elements are 'probably' active/interactable)
 */
public class SiteLoadingTests extends BaseTest
{

@Test
public void siteLoadsTest( )
{
	NavBar navBar = startPage.getNavBar();
	assertTrue(navBar.isSiteTitleDisplayed());
	assertTrue(navBar.isDropdownEnabled());
}
}
