package pages;

import components.LocationAnalysisControlBar;
import org.openqa.selenium.WebDriver;
import pages.base.BaseAnalysisPage;

/**
 * POM representation of page for analysis of some location
 */
public class LocationAnalysisPage extends BaseAnalysisPage<LocationAnalysisControlBar>
{

	public LocationAnalysisPage( final WebDriver driver )
	{
		super(driver, "Analyze Location");
		this.controlBar = new LocationAnalysisControlBar(driver);
	}
}
