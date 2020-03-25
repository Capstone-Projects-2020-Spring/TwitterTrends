package ui.pages;

import ui.components.NetworkAnalysisControlBar;
import org.openqa.selenium.WebDriver;
import ui.pages.base.BaseAnalysisPage;

/**
 * POM representation of page for analysis of some person's network
 */
public class NetworkAnalysisPage extends BaseAnalysisPage<NetworkAnalysisControlBar>
{

	public NetworkAnalysisPage( final WebDriver driver )
	{
		super(driver, "Analyze Network");
		this.controlBar = new NetworkAnalysisControlBar(driver);
	}
}
