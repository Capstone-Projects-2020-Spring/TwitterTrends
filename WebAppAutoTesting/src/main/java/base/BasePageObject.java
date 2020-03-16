package base;

import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.util.List;

/**
 * this contains utility functions needed by most or all classes which represent entities on the website (based on the
 * Page Object Model (POM))
 */
public class BasePageObject
{
protected static final int MAX_TIMEOUT = 60;
protected static final int TEST_CHECK_TIMEOUT = 10;

protected static final String JS_GET_DOC_READY_STATE = "return document.readyState;";
protected static final String JS_GET_JQUERY_LOADED
	= "return !( (typeof jQuery == 'undefined') || (typeof jQuery == 'function') );";
protected static final String JS_GET_ANGULAR_LOADED
	= "return !( (typeof angular == 'undefined') || (typeof angular == 'function') );";
private static final boolean IS_ANGULAR_NEEDED = false;

protected WebDriver driver;

protected BasePageObject( final WebDriver driver )
{
	this.driver = driver;
	waitForPageLoad();
}

// |||||||||||||||||||||||||| DATA RETRIEVAL UTILITIES ||||||||||||||||||||||||

/**
 * retrieves the text of a displayed element
 *
 * Note- this trims whitespace off the ends of the retrieved string
 *
 * @param elem an element which is or soon will be displayed
 *
 * @return the human-visible text of that element
 */
protected String getText( final WebElement elem )
{
	waitForElementDisplayed(elem);
	String elemText = elem.getText();
	elemText = elemText.trim();
	return elemText;
}

/**
 * overloads {@link #getText(WebElement)} to fetch the element based on a locator
 */
protected String getText( final By loc )
{
	WebElement elem = getElement(loc);
	return getText(elem);
}

/**
 * determines whether any element matching the given locator is loaded or loads within a short time
 *
 * @param loc description of the element which should be loaded
 *
 * @return whether any element matching the given locator is loaded or loads within a short time
 */
protected boolean checkForElement( final By loc )
{
	ExpectedCondition<Boolean> isPresent = webDriver ->
	{
		assert webDriver != null;
		WebElement elem = webDriver.findElement(loc);
		return elem != null;
	};
	return checkForCond(isPresent);
}

/**
 * overloads {@link #checkForElement(By)} to look for the element inside of a container element
 */
protected boolean checkForElement( final By loc, final WebElement container )
{
	ExpectedCondition<Boolean> isPresent = webDriver ->
	{
		WebElement elem = container.findElement(loc);
		return elem != null;
	};
	return checkForCond(isPresent);
}

/**
 * determines whether any element matching the given locator exists and is displayed or becomes so within a short time
 *
 * @param loc description of the element which should be loaded and displayed
 *
 * @return whether any element matching the given locator is exists and is displayed or becomes so within a short time
 */
protected boolean checkForDisplayedElement( final By loc )
{
	ExpectedCondition<Boolean> isDisplayed = webDriver ->
	{
		assert webDriver != null;
		WebElement elem = webDriver.findElement(loc);
		return elem.isDisplayed();
	};
	return checkForCond(isDisplayed);
}

/**
 * overloads {@link #checkForDisplayedElement(By)} to look for the element inside of a container element
 */
protected boolean checkForDisplayedElement( final By loc, final WebElement container )
{
	ExpectedCondition<Boolean> isDisplayed = webDriver ->
	{
		WebElement elem = container.findElement(loc);
		return elem.isDisplayed();
	};
	return checkForCond(isDisplayed);
}

/**
 * determines whether any element matching the given locator exists and is enabled or becomes so within a short time
 *
 * @param loc description of the element which should be loaded and enabled
 *
 * @return whether any element matching the given locator is exists and is enabled or becomes so within a short time
 */
protected boolean checkForEnabledElement( final By loc )
{
	ExpectedCondition<Boolean> isEnabled = webDriver ->
	{
		assert webDriver != null;
		WebElement elem = webDriver.findElement(loc);
		return elem.isEnabled();
	};
	return checkForCond(isEnabled);
}

/**
 * overloads {@link #checkForEnabledElement(By)} to look for the element inside of a container element
 */
protected boolean checkForEnabledElement( final By loc, final WebElement container )
{
	ExpectedCondition<Boolean> isEnabled = webDriver ->
	{
		WebElement elem = container.findElement(loc);
		return elem.isEnabled();
	};
	return checkForCond(isEnabled);
}

//todo add functions which take a webelement and 'check' if it is displayed or enabled or else becomes so in a window of time

// |||||||||||||||||||||||||| INTERACTION UTILITIES ||||||||||||||||||||||||

/**
 * enters the given text into the given element and might then press enter
 *
 * @param targetElem the text field
 * @param text       the text to be entered
 * @param pressEnter whether to press enter after entering the text
 */
protected void enterText( final WebElement targetElem, final String text, final boolean pressEnter )
{
	waitForElementEnabled(targetElem);
	targetElem.sendKeys(text);
	if ( pressEnter ) { targetElem.sendKeys(Keys.ENTER); }
	waitForPageLoad();//todo is necessary?
}

/**
 * overloads {@link #enterText(WebElement, String, boolean)} to always press enter
 */
protected void enterText( final WebElement targetElem, final String text ) { enterText(targetElem, text, true);}

/**
 * overloads {@link #enterText(WebElement, String, boolean)} to fetch element based on locator
 */
protected void enterText( final By targetLoc, final String text, final boolean pressEnter )
{
	WebElement elem = getElement(targetLoc);
	enterText(elem, text, pressEnter);
}

/**
 * overloads {@link #enterText(By, String, boolean)} to always press enter
 */
protected void enterText( final By targetLoc, final String text ) { enterText(targetLoc, text, true); }

/**
 * waits for an element to be enabled, clicks it,
 * and then tries to make sure the page finishes reloading or loading a new page
 *
 * @param elem the element which should be clicked
 */
protected void clickElem( final WebElement elem )
{
	waitForElementEnabled(elem);
	elem.click();
	waitForPageLoad();
}

/**
 * overloads {@link #clickElem(WebElement)} to fetch element based on locator
 */
protected void clickElem( final By loc )
{
	WebElement elem = getElement(loc);
	clickElem(elem);
}

// |||||||||||||||||||||||||| WAIT UTILITIES ||||||||||||||||||||||||

/**
 * waits for an element matching the locator to be present and then fetches/returns it
 *
 * @param loc description of the desired element
 *
 * @return the element
 */
protected WebElement getElement( final By loc )
{
	ExpectedCondition<WebElement> elementLoaded = webDriver ->
	{
		assert webDriver != null;
		WebElement loadedElem = webDriver.findElement(loc);
		return loadedElem;
	};
	WebElement elem = waitForCond(elementLoaded);
	return elem;
}

/**
 * overloads {@link #getElement(By)} to look for the element inside of a container element
 */
protected WebElement getElement( final By loc, final WebElement container )
{
	ExpectedCondition<WebElement> elementLoaded = webDriver ->
	{
		WebElement loadedElem = container.findElement(loc);
		return loadedElem;
	};
	WebElement elem = waitForCond(elementLoaded);
	return elem;
}

/**
 * waits for one or more elements matching the locator to be present and then fetches/returns them
 *
 * @param loc description of the desired elements
 *
 * @return the elements
 */
protected List<WebElement> getElements( final By loc )
{
	ExpectedCondition<List<WebElement>> elementsLoaded = webDriver ->
	{
		assert webDriver != null;
		List<WebElement> loadedElems = webDriver.findElements(loc);
		return loadedElems;
	};
	List<WebElement> elems = waitForCond(elementsLoaded);
	return elems;
}

/**
 * overloads {@link #getElements(By)} to look for the elements inside of a container element
 */
protected List<WebElement> getElements( final By loc, final WebElement container )
{
	ExpectedCondition<List<WebElement>> elementsLoaded = webDriver ->
	{
		List<WebElement> loadedElems = container.findElements(loc);
		return loadedElems;
	};
	List<WebElement> elems = waitForCond(elementsLoaded);
	return elems;
}

/**
 * waits for an element matching the locator to be present & displayed and then fetches/returns it
 *
 * @param loc description of the desired element
 *
 * @return the element
 */
protected WebElement getDisplayedElement( final By loc )
{
	ExpectedCondition<WebElement> elementDisplayed = webDriver ->
	{
		assert webDriver != null;
		WebElement displayedElem = webDriver.findElement(loc);
		if ( !displayedElem.isDisplayed() ) {displayedElem = null;}
		return displayedElem;
	};
	WebElement elem = waitForCond(elementDisplayed);
	return elem;
}

/**
 * overloads {@link #getDisplayedElement(By)} to look for the element inside of a container element
 */
protected WebElement getDisplayedElement( final By loc, final WebElement container )
{
	ExpectedCondition<WebElement> elementDisplayed = webDriver ->
	{
		WebElement displayedElem = container.findElement(loc);
		if ( !displayedElem.isDisplayed() ) {displayedElem = null;}
		return displayedElem;
	};
	WebElement elem = waitForCond(elementDisplayed);
	return elem;
}

/**
 * waits for one or more elements matching the locator to be present & displayed and then fetches/returns them
 *
 * @param loc description of the desired elements
 *
 * @return the elements
 */
protected List<WebElement> getDisplayedElements( final By loc )
{
	ExpectedCondition<List<WebElement>> elementsLoaded = webDriver ->
	{
		assert webDriver != null;
		List<WebElement> displayedElems = webDriver.findElements(loc);
		boolean isAnyDisplayed = displayedElems.stream()
											   .anyMatch(WebElement::isDisplayed);
		if ( !isAnyDisplayed ) { displayedElems = null; }
		return displayedElems;
	};
	List<WebElement> elems = waitForCond(elementsLoaded);
	return elems;
}

/**
 * overloads {@link #getDisplayedElements(By)} to look for the elements inside of a container element
 */
protected List<WebElement> getDisplayedElements( final By loc, final WebElement container )
{
	ExpectedCondition<List<WebElement>> elementsLoaded = webDriver ->
	{
		List<WebElement> displayedElems = container.findElements(loc);
		boolean isAnyDisplayed = displayedElems.stream()
											   .anyMatch(WebElement::isDisplayed);
		if ( !isAnyDisplayed ) { displayedElems = null; }
		return displayedElems;
	};
	List<WebElement> elems = waitForCond(elementsLoaded);
	return elems;
}

/**
 * waits for an element matching the locator to be present, displayed, and enabled* and then fetches/returns it
 *
 * *if an element's 'enabled' then it can probably be clicked on or otherwise interacted with
 *
 * @param loc description of the desired element
 *
 * @return the element
 */
protected WebElement getEnabledElement( final By loc )
{
	ExpectedCondition<WebElement> elementEnabled = webDriver ->
	{
		assert webDriver != null;
		WebElement enabledElem = webDriver.findElement(loc);
		if ( !(enabledElem.isDisplayed() && enabledElem.isEnabled()) ) {enabledElem = null;}
		return enabledElem;
	};
	WebElement elem = waitForCond(elementEnabled);
	return elem;
}

/**
 * overloads {@link #getEnabledElement(By)} to look for the element inside of a container element
 */
protected WebElement getEnabledElement( final By loc, final WebElement container )
{
	ExpectedCondition<WebElement> elementEnabled = webDriver ->
	{
		WebElement enabledElem = container.findElement(loc);
		if ( !(enabledElem.isDisplayed() && enabledElem.isEnabled()) ) {enabledElem = null;}
		return enabledElem;
	};
	WebElement elem = waitForCond(elementEnabled);
	return elem;
}

/**
 * waits for one or more elements matching the locator to be present, displayed, and enabled* and then fetches/returns
 * them
 *
 * *if an element's 'enabled' then it can probably be clicked on or otherwise interacted with
 *
 * @param loc description of the desired elements
 *
 * @return the elements
 */
protected List<WebElement> getEnabledElements( final By loc )
{
	ExpectedCondition<List<WebElement>> elementsLoaded = webDriver ->
	{
		assert webDriver != null;
		List<WebElement> enabledElems = webDriver.findElements(loc);
		boolean isAnyEnabled = enabledElems.stream()
										   .anyMatch(elem -> elem.isDisplayed() && elem.isEnabled());
		if ( !isAnyEnabled ) { enabledElems = null; }
		return enabledElems;
	};
	List<WebElement> elems = waitForCond(elementsLoaded);
	return elems;
}

/**
 * overloads {@link #getEnabledElements(By)} to look for the elements inside of a container element
 */
protected List<WebElement> getEnabledElements( final By loc, final WebElement container )
{
	ExpectedCondition<List<WebElement>> elementsLoaded = webDriver ->
	{
		List<WebElement> enabledElems = container.findElements(loc);
		boolean isAnyEnabled = enabledElems.stream()
										   .anyMatch(elem -> elem.isDisplayed() && elem.isEnabled());
		if ( !isAnyEnabled ) { enabledElems = null; }
		return enabledElems;
	};
	List<WebElement> elems = waitForCond(elementsLoaded);
	return elems;
}

//todo add functions which take webelement and wait for it to be displayed or displayed/enabled with variable timeout?

/**
 * waits for a loaded element to be displayed
 *
 * @param elem element which should be displayed
 */
protected void waitForElementDisplayed( final WebElement elem )
{
	ExpectedCondition<Boolean> elementDisplayed = webDriver ->
	{
		return elem.isDisplayed();
	};
	waitForCond(elementDisplayed);
}

/**
 * waits for a loaded element to be enabled
 *
 * @param elem element which should be enabled
 */
protected void waitForElementEnabled( final WebElement elem )
{
	ExpectedCondition<Boolean> elementEnabled = webDriver ->
	{
		return elem.isDisplayed() && elem.isEnabled();
	};
	waitForCond(elementEnabled);
}

/**
 * waits up to some length of time for a condition to become true,
 * either returning as soon as it becomes true or throwing an exception when the timeout is reached
 *
 * @param condition the condition to wait for
 * @param timeout   how long to wait before timing out
 */
private <T> T waitForCond( final ExpectedCondition<T> condition, final int timeout )
{
	WebDriverWait waiter = new WebDriverWait(driver, timeout);
	T result = waiter.until(condition);
	
	return result;
}

/**
 * overloads {@link #waitForCond(ExpectedCondition, int)} to always use the max timeout
 */
private <T> T waitForCond( final ExpectedCondition<T> condition ) { return waitForCond(condition, MAX_TIMEOUT); }

/**
 * checks whether some condition is true or becomes true within some amount of time
 *
 * @param condition the condition to check for
 * @param waitLen   the maximum time to wait for the condition to become true
 *
 * @return whether the condition is true or becomes true within the given amount of time
 */
private boolean checkForCond( final ExpectedCondition<Boolean> condition, final int waitLen )
{
	boolean wasConditionSatisfied = true;
	
	WebDriverWait testWaiter = new WebDriverWait(driver, waitLen);
	try
	{
		testWaiter.until(condition);
	}
	catch ( TimeoutException e )
	{
		wasConditionSatisfied = false;
	}
	return wasConditionSatisfied;
}

/**
 * overloads {@link #checkForCond(ExpectedCondition, int)} to always use the standard testing wait length
 */
private boolean checkForCond( final ExpectedCondition<Boolean> condition )
{
	return checkForCond(condition, TEST_CHECK_TIMEOUT);
}

// |||||||||||||||||||||||||| PAGE LOAD UTILITIES ||||||||||||||||||||||||

/**
 * waits for the page to finish loading
 */
public void waitForPageLoad( )
{
	final int sleepDuration = 20;//milliseconds
	
	ExpectedCondition<Boolean> pageLoaded = webDriver ->
	{
		return isDocumentReady();
	};
	waitForCond(pageLoaded);
	
	if ( !isJqueryReady() ) { sleep(sleepDuration); }
	if ( IS_ANGULAR_NEEDED && !isAngularReady() ) { sleep(sleepDuration); }
	if ( !isJqueryReady() ) { sleep(sleepDuration); }
	if ( IS_ANGULAR_NEEDED && !isAngularReady() ) { sleep(sleepDuration); }
}

/**
 * extra-safe version of {@link #waitForPageLoad()} which makes sure the old page is gone before starting
 * to wait for the new page to load
 * This avoids a race condition where normal waitForPageLoad() gets to check whether the page is loaded before the
 * old page has been 'unloaded', and so the wait ends very prematurely
 *
 * @param oldElem a reference to an element on the old webpage which is being left
 */
protected void waitForPageLoad( final WebElement oldElem )
{
	waitForCond(ExpectedConditions.stalenessOf(oldElem));
	waitForPageLoad();
}

private boolean isDocumentReady( )
{
	boolean isDocReady = false;
	String docReadyState = (String) executeJs(JS_GET_DOC_READY_STATE);
	isDocReady = docReadyState.equals("complete") || docReadyState.equals("loaded");
	return isDocReady;
}

private boolean isJqueryReady( )
{
	boolean isJqReady = (Boolean) executeJs(JS_GET_JQUERY_LOADED);
	return isJqReady;
}

private boolean isAngularReady( )
{
	boolean isAngReady = (Boolean) executeJs(JS_GET_ANGULAR_LOADED);
	return isAngReady;
}

private Object executeJs( final String jsCode )
{
	Object retVal = null;
	JavascriptExecutor jsExec = (JavascriptExecutor) driver;
	retVal = jsExec.executeScript(jsCode);
	return retVal;
}

protected void sleep( final int millis )
{
	try { Thread.sleep(millis); }
	catch ( InterruptedException e ) { System.err.println("WARN- Interrupted during sleep"); }
}
}
