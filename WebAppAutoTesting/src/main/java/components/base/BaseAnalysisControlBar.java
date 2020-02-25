package components.base;

import org.openqa.selenium.WebDriver;

/**
 * POM representation of elements common to the analysis control bars on all 'Analyze _' pages
 */
public abstract class BaseAnalysisControlBar extends BaseComponent
{

	protected BaseAnalysisControlBar( final WebDriver driver )
	{
		super(driver);
	}
}
