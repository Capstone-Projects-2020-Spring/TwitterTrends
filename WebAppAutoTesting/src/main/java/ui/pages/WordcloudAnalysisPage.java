package ui.pages;

import org.openqa.selenium.WebDriver;
import ui.components.WordcloudAnalysisControlBar;
import ui.pages.base.BaseAnalysisPage;

/**
 * POM representation of page for word cloud visualization of common terms in tweets by people in a person's network
 */
public class WordcloudAnalysisPage extends BaseAnalysisPage<WordcloudAnalysisControlBar>
{

public WordcloudAnalysisPage( final WebDriver driver )
{
	super(driver, "Word Cloud");
	this.controlBar = new WordcloudAnalysisControlBar(driver);
}
}