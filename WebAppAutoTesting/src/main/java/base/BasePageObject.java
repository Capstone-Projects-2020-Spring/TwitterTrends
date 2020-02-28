package base;

import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * this contains utility functions needed by most or all classes which represent entities on the website (based on the
 * Page Object Model (POM))
 */
public class BasePageObject
{
protected static final int MAX_TIMEOUT = 60;

protected static final String JS_GET_DOC_READY_STATE = "return document.readyState;";
protected static final String JS_GET_JQUERY_LOADED
	= "return !( (typeof jQuery == 'undefined') || (typeof jQuery == 'function') );";
protected static final String JS_GET_ANGULAR_LOADED
	= "return !( (typeof angular == 'undefined') || (typeof angular == 'function') );";
private static final boolean IS_ANGULAR_NEEDED = false;

protected WebDriver driver;
private WebDriverWait waiter;

protected BasePageObject( final WebDriver driver )
{
	this.driver = driver;
	this.waiter = new WebDriverWait(driver, MAX_TIMEOUT);
	
	waitForPageLoad();
}

// |||||||||||||||||||||||||| DATA RETRIEVAL UTILITIES ||||||||||||||||||||||||

/**
 * retrieves the text of a displayed element
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
	WebElement elem = waiter.until(elementLoaded);
	return elem;
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
		WebElement elem = waiter.until(elementDisplayed);
		return elem;
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
		if ( !enabledElem.isEnabled() ) {enabledElem = null;}
		return enabledElem;
	};
	WebElement elem = waiter.until(elementEnabled);
	return elem;
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
	waiter.until(elementDisplayed);
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
		return elem.isEnabled();
	};
	waiter.until(elementEnabled);
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
	waiter.until(pageLoaded);
	
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
	waiter.until(ExpectedConditions.stalenessOf(oldElem));
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
