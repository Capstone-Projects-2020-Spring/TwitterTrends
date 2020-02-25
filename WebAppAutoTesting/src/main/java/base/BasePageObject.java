package base;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
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
	protected static final String JS_GET_JQUERY_LOAD_STATE
		= "return !( (typeof jQuery == 'undefined') || (typeof jQuery == 'function') );";
	protected static final String JS_GET_ANGULAR_LOAD_STATE
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
	public void waitForPageLoad( final WebElement oldElem )
	{
		waiter.until(ExpectedConditions.stalenessOf(oldElem));
		waitForPageLoad();
	}

	/**
	 * waits for an element matching the locator to be present and then fetches/returns it
	 *
	 * @param loc description of the desired element
	 *
	 * @return the element
	 */
	public WebElement waitForElementPresent( final By loc )
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
	public WebElement waitForElementDisplayed( final By loc )
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
	public WebElement waitForElementEnabled( final By loc )
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

	private boolean isDocumentReady( )
	{
		boolean isDocReady = false;
		String docReadyState = (String) executeJs(JS_GET_DOC_READY_STATE);
		isDocReady = docReadyState.equals("complete") || docReadyState.equals("loaded");
		return isDocReady;
	}

	private boolean isJqueryReady( )
	{
		boolean isJqReady = (Boolean) executeJs(JS_GET_JQUERY_LOAD_STATE);
		return isJqReady;
	}

	private boolean isAngularReady( )
	{
		boolean isAngReady = (Boolean) executeJs(JS_GET_ANGULAR_LOAD_STATE);
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
