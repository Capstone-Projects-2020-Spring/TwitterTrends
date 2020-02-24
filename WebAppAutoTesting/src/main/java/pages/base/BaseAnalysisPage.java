package pages.base;

import components.BaseAnalysisControlBar;

/**
 * POM representation of shared components among 'Analyze _' pages on the website
 */
public abstract class BaseAnalysisPage<T extends BaseAnalysisControlBar> extends BasePage
{
	protected T controlBar;

	public T getControlBar( ) { return controlBar; }
}
