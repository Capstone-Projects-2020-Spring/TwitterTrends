package api.responses;

import com.google.gson.annotations.SerializedName;

/**
 * stores information about a trend sent from the backend server
 */
public class Trend
{
@SerializedName(value = "trend_PK")
protected int trendPk;

protected String trendContent;
protected boolean isHashtag;
protected String queryTerm;
protected int tweetVolume;

public Trend( ) {}

public Trend( final int trendPk, final String trendContent, final boolean isHashtag, final String queryTerm,
	final int tweetVolume )
{
	this.trendPk = trendPk;
	this.trendContent = trendContent;
	this.isHashtag = isHashtag;
	this.queryTerm = queryTerm;
	this.tweetVolume = tweetVolume;
}

public int getTrendPk( )
{
	return trendPk;
}

public void setTrendPk( final int trendPk )
{
	this.trendPk = trendPk;
}

public String getTrendContent( )
{
	return trendContent;
}

public void setTrendContent( final String trendContent )
{
	this.trendContent = trendContent;
}

public boolean isHashtag( )
{
	return isHashtag;
}

public void setHashtag( final boolean hashtag )
{
	isHashtag = hashtag;
}

public String getQueryTerm( )
{
	return queryTerm;
}

public void setQueryTerm( final String queryTerm )
{
	this.queryTerm = queryTerm;
}

public int getTweetVolume( )
{
	return tweetVolume;
}

public void setTweetVolume( final int tweetVolume )
{
	this.tweetVolume = tweetVolume;
}
}
