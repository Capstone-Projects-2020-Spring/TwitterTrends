package pages;

import components.TimeAnalysisControlBar;
import org.openqa.selenium.WebDriver;
import pages.base.BaseAnalysisPage;

/**
 * POM representation of page for analysis of some time period
 */
public class TimeAnalysisPage extends BaseAnalysisPage<TimeAnalysisControlBar>
{

	public TimeAnalysisPage( final WebDriver driver )
	{
		super(driver, "Analyze Time");
		this.controlBar = new TimeAnalysisControlBar(driver);
	}
}
