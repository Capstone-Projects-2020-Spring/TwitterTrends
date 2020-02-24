package pages;

import components.LocationAnalysisControlBar;
import pages.base.BaseAnalysisPage;

/**
 * POM representation of page for analysis of some location
 */
public class LocationAnalysisPage extends BaseAnalysisPage<LocationAnalysisControlBar>
{

	public LocationAnalysisPage( )
	{
		this.controlBar = new LocationAnalysisControlBar();
	}
}
