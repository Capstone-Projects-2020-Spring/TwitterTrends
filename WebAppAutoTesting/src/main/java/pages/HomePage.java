package pages;

import components.HomePageNavBar;
import org.openqa.selenium.WebDriver;
import pages.base.BasePage;

/**
 * POM representation of the starting page of the website
 */
public class HomePage extends BasePage<HomePageNavBar>
{

public HomePage( final WebDriver driver )
{
	super(driver);
	navBar = new HomePageNavBar(driver);
}
}
