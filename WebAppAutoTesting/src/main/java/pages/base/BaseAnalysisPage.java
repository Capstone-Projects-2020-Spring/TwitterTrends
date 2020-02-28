package pages.base;

import components.NavBar;
import components.base.BaseAnalysisControlBar;
import org.openqa.selenium.WebDriver;

/**
 * POM representation of shared components among 'Analyze _' pages on the website
 */
public abstract class BaseAnalysisPage<T extends BaseAnalysisControlBar> extends BasePage<NavBar>
{
protected T controlBar;

protected BaseAnalysisPage( final WebDriver driver )
{
	super(driver);
	this.navBar = new NavBar(driver);
}

public T getControlBar( ) { return controlBar; }
}
