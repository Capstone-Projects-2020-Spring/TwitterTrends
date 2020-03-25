package ui.enums;

import ui.components.base.BaseAnalysisControlBar;
import org.openqa.selenium.WebDriver;
import ui.pages.LocationAnalysisPage;
import ui.pages.NetworkAnalysisPage;
import ui.pages.TimeAnalysisPage;
import ui.pages.base.BaseAnalysisPage;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

/**
 * describes the different analysis ui.pages on the website
 */
public enum AnalysisPages
{
	//todo
	TIME("Time", TimeAnalysisPage.class),
	LOCATION("Location", LocationAnalysisPage.class),
	NETWORK("Network", NetworkAnalysisPage.class);

private String dropdownOptionText;
private Class<? extends BaseAnalysisPage<? extends BaseAnalysisControlBar>> pageClass;

<T extends BaseAnalysisPage<? extends BaseAnalysisControlBar>> AnalysisPages( final String navBarOptionText,
	final Class<T> linkedPageClass )
{
	this.dropdownOptionText = navBarOptionText;
	this.pageClass = linkedPageClass;
}

public String getDropdownOptionText( ) { return dropdownOptionText; }

/**
 * generate an instance of the POM representation of the analysis page which the current enum entry describes
 *
 * @param driver the Webdriver which is used to interact with ui.pages
 * @param <T>    the type of the POM representation of the analysis page which the current enum entry describes
 *
 * @return an instance of the POM representation of the analysis page which the current enum entry describes
 */
public <T extends BaseAnalysisPage<? extends BaseAnalysisControlBar>> T getPageInstance( final WebDriver driver )
{
	T newPage = null;
	try
	{
		Constructor<T> pageConstructor = (Constructor<T>) pageClass.getConstructor(WebDriver.class);
		newPage = pageConstructor.newInstance(driver);
	}
	catch ( NoSuchMethodException | InstantiationException | IllegalAccessException | InvocationTargetException e )
	{
		System.err.println("FATAL- PAGE CLASS" + dropdownOptionText + " NOT INSTANTIABLE");
		System.exit(1);
	}
	
	return newPage;
}
}
