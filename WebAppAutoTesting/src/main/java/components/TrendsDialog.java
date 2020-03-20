package components;

import components.base.BaseComponent;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

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
 * retrieves the top trends and strips off the index at the beginning of each
 *
 * @return the top trends without the popup's index numbers at the start of each
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
		if ( elemText.matches(trendEntryTemplate) )
		{
			//cut out the starting template with the entry index
			elemText = elemText.substring(3);
			trends.add(elemText);
		}
		else { trends.add(null); }
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
	if ( entryIndex < 1 || entryIndex > 5 )
	{
		throw new IllegalArgumentException("there is never a trend entry with index " + entryIndex);
	}
	String trendEntryClass = String.format("trend-%d", entryIndex);
	By trendEntryLoc = By.className(trendEntryClass);
	return trendEntryLoc;
}
}
