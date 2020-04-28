package ui.components;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedCondition;
import ui.components.base.BaseComponent;

import java.util.ArrayList;
import java.util.List;

/**
 * this represents the popup which shows the top trends for a location
 */
public class TrendsDialog extends BaseComponent
{

public static final int MIN_TREND_ENTRY_INDEX = 1;
public static final int MAX_TREND_ENTRY_INDEX = 5;
final protected By popupContainerLoc = By.id("bg-modal");
final protected By popupCloseButton = By.id("close");
final protected By popupTitle = By.className("top-trends-title");
final protected By popupTrendsList = By.className("top-trends-ul");
final protected By trendEntry = By.tagName("span");

final protected static String STYLE_ATTRIBUTE_NAME = "style";
final protected static String HIDDEN_ELEMENT_STYLE_DISPLAY = "display: none";

public TrendsDialog( final WebDriver driver )
{
	super(driver);
}

/**
 * closes/hides the dialog
 */
public void closeDialog( )
{
	clickElem(popupCloseButton);
	waitForCond(webDriver ->
	{
		boolean isClosed = false;
		WebElement dialogElem = getElement(popupContainerLoc);
		String dialogStyle = getAttribute(dialogElem, STYLE_ATTRIBUTE_NAME);
		isClosed = dialogStyle.isEmpty() || dialogStyle.contains(HIDDEN_ELEMENT_STYLE_DISPLAY);
		return isClosed;
	});
}

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
		boolean areTrendsLoaded = true;
		
		List<String> trends = getTopTrends();
		if ( trends == null )
		{
			areTrendsLoaded = false;
		} else
		{
			for ( String trend : trends )
			{
				if ( "".equals(trend) )
				{
					areTrendsLoaded = false;
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
 * gets a locator for a particular entry in the list of top trends
 *
 * @param entryIndex the index of the top trend whose locator should be built
 *
 * @return a locator for a particular entry in the list of top trends
 */
protected By getPopupTrendEntryLoc( final int entryIndex )
{
	if ( entryIndex < MIN_TREND_ENTRY_INDEX || entryIndex > MAX_TREND_ENTRY_INDEX )
	{
		throw new IllegalArgumentException("there is never a trend entry with index " + entryIndex);
	}
	String trendEntryClass = String.format("trend-%d", entryIndex);
	By trendEntryLoc = By.className(trendEntryClass);
	return trendEntryLoc;
}
}
