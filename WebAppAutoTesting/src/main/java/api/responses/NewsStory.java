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

public NewsStory( ) {}

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

public String getTitle( )
{
	return title;
}

public void setTitle( final String title )
{
	this.title = title;
}

public String getAuthor( )
{
	return author;
}

public void setAuthor( final String author )
{
	this.author = author;
}

public String getSourceName( )
{
	return sourceName;
}

public void setSourceName( final String sourceName )
{
	this.sourceName = sourceName;
}

public String getLinkUrl( )
{
	return linkUrl;
}

public void setLinkUrl( final String linkUrl )
{
	this.linkUrl = linkUrl;
}

public String getDate( )
{
	return date;
}

public void setDate( final String date )
{
	this.date = date;
}

public String getDescription( )
{
	return description;
}

public void setDescription( final String description )
{
	this.description = description;
}

public String getContentStart( )
{
	return contentStart;
}

public void setContentStart( final String contentStart )
{
	this.contentStart = contentStart;
}
}
