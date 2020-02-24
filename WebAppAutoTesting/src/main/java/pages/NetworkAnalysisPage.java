package pages;

import components.NetworkAnalysisControlBar;
import pages.base.BaseAnalysisPage;

/**
 * POM representation of page for analysis of some person's network
 */
public class NetworkAnalysisPage extends BaseAnalysisPage<NetworkAnalysisControlBar>
{

	public NetworkAnalysisPage( )
	{
		this.controlBar = new NetworkAnalysisControlBar();
	}
}
