package enums;

import components.base.BaseAnalysisControlBar;
import org.openqa.selenium.WebDriver;
import pages.LocationAnalysisPage;
import pages.NetworkAnalysisPage;
import pages.TimeAnalysisPage;
import pages.base.BaseAnalysisPage;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

/**
 * describes the different analysis pages on the website
 */
public enum AnalysisPages
{
	//todo
	TIME(null, TimeAnalysisPage.class),
	LOCATION(null, LocationAnalysisPage.class),
	NETWORK(null, NetworkAnalysisPage.class);

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
 * @param driver the Webdriver which is used to interact with pages
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
