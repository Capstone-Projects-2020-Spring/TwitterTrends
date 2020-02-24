package pages;

import components.TimeAnalysisControlBar;
import pages.base.BaseAnalysisPage;

/**
 * POM representation of page for analysis of some time period
 */
public class TimeAnalysisPage extends BaseAnalysisPage<TimeAnalysisControlBar>
{

	public TimeAnalysisPage( )
	{
		this.controlBar = new TimeAnalysisControlBar();
	}
}
