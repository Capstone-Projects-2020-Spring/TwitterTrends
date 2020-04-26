package ui.enums;

import org.openqa.selenium.WebDriver;
import ui.pages.*;
import ui.pages.base.BasePage;

import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

/**
 * describes the different pages on the website
 */
public enum TwitterTrendsPages
{
	TIME("Time", TimeAnalysisPage.class),
	//this needs to not be first because this refers to the home page and some tests cycle through the pages listed here, starting with the home page
	LOCATION("Location", HomePage.class),
	NETWORK("Network", NetworkAnalysisPage.class),
	WORDCLOUD("Word Cloud", WordcloudAnalysisPage.class),
	EXPLORATION("Tweets/Trends", ExplorationPage.class),
	HELP("Help", HelpPage.class);

private String dropdownOptionText;
private Class<? extends BasePage> pageClass;

<T extends BasePage> TwitterTrendsPages( final String navBarOptionText, final Class<T> linkedPageClass )
{
	this.dropdownOptionText = navBarOptionText;
	this.pageClass = linkedPageClass;
}

public String getDropdownOptionText( ) { return dropdownOptionText; }

/**
 * generate an instance of the POM representation of the page which the current enum entry describes
 *
 * @param driver the Webdriver which is used to interact with ui.pages
 * @param <T>    the type of the POM representation of the analysis page which the current enum entry describes
 *
 * @return an instance of the POM representation of the analysis page which the current enum entry describes
 */
public <T extends BasePage> T getPageInstance( final WebDriver driver )
{
	T newPage = null;
	try
	{
		Constructor<T> pageConstructor = (Constructor<T>) pageClass.getConstructor(WebDriver.class);
		newPage = pageConstructor.newInstance(driver);
	} catch ( NoSuchMethodException | InstantiationException | IllegalAccessException | InvocationTargetException e )
	{
		System.err.println("FATAL- PAGE CLASS " + dropdownOptionText + " NOT INSTANTIABLE");
		throw new RuntimeException("Unable to instantiate " + this.pageClass.toString());
	}
	
	return newPage;
}
}
