package components;

import components.base.BaseComponent;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedCondition;

import java.util.ArrayList;
import java.util.List;

/**
 * this represents the popup which shows the top trends for a location
 */
public class TrendsDialog extends BaseComponent
{

final protected By popupContainerLoc = By.id("bg-modal");
final protected By popupCloseButton = By.id("close");
final protected By popupTitle = By.className("top-trends-title");
final protected By popupTrendsList = By.className("top-trends-ul");
final protected By trendEntry = By.tagName("li");
final protected String trendEntryTemplate = "[1-5]\\. .+";

public TrendsDialog( final WebDriver driver )
{
	super(driver);
}

/**
 * closes/hides the dialog
 */
public void closeDialog( ) { clickElem(popupCloseButton);}

/**
 * Overloads {@link #waitForTrendsLoaded(int)} to wait for the standard maximum timeout
 */
public void waitForTrendsLoaded( ) { waitForTrendsLoaded(MAX_TIMEOUT); }

/**
 * waits for up to some number of seconds for trends to load in the dialog
 *
 * @param timeout the maximum number of seconds to wait before timing out
 */
public void waitForTrendsLoaded( final int timeout )
{
	ExpectedCondition<Boolean> trendsLoaded = webdriver ->
	{
		boolean areTrendsLoaded = false;
		
		List<String> trendLineStrs = getTopTrends();
		List<String> trends = cleanTrends(trendLineStrs);
		if ( trends != null )
		{
			for ( String trend : trends )
			{
				if ( !"".equals(trend) )
				{
					areTrendsLoaded = true;
					break;
				}
			}
		}
		
		return areTrendsLoaded;
	};
	waitForCond(trendsLoaded, timeout);
}

/**
 * retrieves the top trends
 *
 * @return the top trends with the popup's index numbers at the start of each
 */
public List<String> getTopTrends( )
{
	List<String> trends = new ArrayList<>();
	
	WebElement popupContainer = getElement(popupContainerLoc);
	//waits for contents of popup to be displayed
	getDisplayedElement(popupTitle, popupContainer);
	WebElement trendsListContainer = getElement(popupTrendsList, popupContainer);
	
	List<WebElement> trendElems = getDisplayedElements(trendEntry, trendsListContainer);
	for ( WebElement elem : trendElems )
	{
		String elemText = getText(elem);
		trends.add(elemText);
	}
	return trends;
}

/**
 * checks whether this is displayed
 *
 * @return whether this is displayed
 */
public boolean isTrendPopupDisplayed( )
{
	WebElement popupContainer = getElement(popupContainerLoc);
	return checkForDisplayedElement(popupTitle, popupContainer);
}

/**
 * clicks on one of the top trends to see more detail about it
 *
 * @param trendIndex the index of the top trend which should be clicked
 */
public void clickTrend( final int trendIndex )
{
	WebElement popupContainer = getElement(popupContainerLoc);
	By trendLoc = getPopupTrendEntryLoc(trendIndex);
	WebElement trendElem = getDisplayedElement(trendLoc, popupContainer);
	clickElem(trendElem);
}

/**
 * strips the index off of the beginning of each trend in the given list of trends
 *
 * @param trendStrs a list of the texts for each line in the top trends dialog, including a trend index at the start
 *
 * @return a list of the trend strings themselves without the indexes at the beginning of each
 * returns null if one or more strings didn't have indices at the beginning
 */
public List<String> cleanTrends( List<String> trendStrs )
{
	List<String> cleanedTrends = new ArrayList<>();
	
	for ( String trendStr : trendStrs )
	{
		if ( trendStr.matches(trendEntryTemplate) )
		{
			//cut out the starting template with the entry index
			String trendText = trendStr.substring(3);
			cleanedTrends.add(trendText);
		} else
		{
			cleanedTrends = null;
			break;
		}
	}
	
	return cleanedTrends;
}

/**
 * gets a locator for a particular entry in the list of top trends
 *
 * @param entryIndex the index of the top trend whose locator should be built
 *
 * @return a locator for a particular entry in the list of top trends
 */
protected By getPopupTrendEntryLoc( final int entryIndex )
{
	if ( entryIndex < 1 || entryIndex > 5 )
	{
		throw new IllegalArgumentException("there is never a trend entry with index " + entryIndex);
	}
	String trendEntryClass = String.format("trend-%d", entryIndex);
	By trendEntryLoc = By.className(trendEntryClass);
	return trendEntryLoc;
}
}
