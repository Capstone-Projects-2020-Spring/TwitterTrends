package api.responses;

/**
 * stores information about a new story (which is related to some trend) sent from the backend server
 */
public class NewsStory
{
protected String title;
protected String author;
protected String sourceName;
protected String linkUrl;
protected String date;
protected String description;
protected String contentStart;

public NewsStory( final String title, final String author, final String source_name, final String link_url,
	final String date, final String description, final String content_start )
{
	this.title = title;
	this.author = author;
	this.sourceName = source_name;
	this.linkUrl = link_url;
	this.date = date;
	this.description = description;
	this.contentStart = content_start;
}

public NewsStory( ) {}

public String getTitle( )
{
	return title;
}

public String getAuthor( )
{
	return author;
}

public String getSourceName( )
{
	return sourceName;
}

public String getLinkUrl( )
{
	return linkUrl;
}

public String getDate( )
{
	return date;
}

public String getDescription( )
{
	return description;
}

public String getContentStart( )
{
	return contentStart;
}
}
