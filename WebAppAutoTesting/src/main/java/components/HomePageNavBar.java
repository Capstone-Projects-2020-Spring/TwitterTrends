package components;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

/**
 * POM representation of the navigation/search bar at the top of the home page
 */
public class HomePageNavBar extends NavBar
{

protected By searchFieldLoc = null;//todo

public HomePageNavBar( final WebDriver driver )
{
	super(driver);
}

/**
 * searches the map visualization for something
 *
 * @param searchText description of what should be searched for
 */
public void searchWorld( final String searchText )
{
	WebElement searchField = getEnabledElement(searchFieldLoc);
	enterText(searchField, searchText);
	//todo?
}
}
