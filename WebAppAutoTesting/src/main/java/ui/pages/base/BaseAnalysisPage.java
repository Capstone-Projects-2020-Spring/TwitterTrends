package ui.pages.base;

import org.openqa.selenium.WebDriver;
import ui.components.NavBar;
import ui.components.base.BaseAnalysisControlBar;

/**
 * POM representation of shared ui.components among 'Analyze _' ui.pages on the website
 */
public abstract class BaseAnalysisPage<T extends BaseAnalysisControlBar> extends BasePage
{

protected T controlBar;

protected BaseAnalysisPage( final WebDriver driver, final String titleText )
{
	super(driver, titleText);
	this.navBar = new NavBar(driver);
}

public T getControlBar( ) { return controlBar; }

}
