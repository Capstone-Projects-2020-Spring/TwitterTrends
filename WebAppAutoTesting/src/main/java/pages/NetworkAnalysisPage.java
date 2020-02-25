package pages;

import components.NetworkAnalysisControlBar;
import org.openqa.selenium.WebDriver;
import pages.base.BaseAnalysisPage;

/**
 * POM representation of page for analysis of some person's network
 */
public class NetworkAnalysisPage extends BaseAnalysisPage<NetworkAnalysisControlBar>
{

	public NetworkAnalysisPage( final WebDriver driver )
	{
		super(driver);
		this.controlBar = new NetworkAnalysisControlBar(driver);
	}
}
