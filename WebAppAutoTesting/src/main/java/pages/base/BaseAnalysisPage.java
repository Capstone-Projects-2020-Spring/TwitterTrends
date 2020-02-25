package pages.base;

import components.base.BaseAnalysisControlBar;
import org.openqa.selenium.WebDriver;

/**
 * POM representation of shared components among 'Analyze _' pages on the website
 */
public abstract class BaseAnalysisPage<T extends BaseAnalysisControlBar> extends BasePage
{
	protected T controlBar;

	protected BaseAnalysisPage( final WebDriver driver )
	{
		super(driver);
	}

	public T getControlBar( ) { return controlBar; }
}
