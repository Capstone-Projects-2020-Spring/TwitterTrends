package api.responses;

import com.google.gson.annotations.SerializedName;

/**
 * stores information about a tweet sent from the backend server
 */
public class Tweet
{
@SerializedName(value = "tweet_PK")
protected String tweetPk;

protected String tweetIdStr;
//todo user id?
protected String content;
protected int latitude;
protected int longitude;
protected int locationId;
protected int likes;
protected int quotes;
protected int retweets;
protected int replies;
protected String tweetDate;

public Tweet( ) { }

public Tweet( final String tweetPK, final String tweetIdStr, final String content, final int latitude,
	final int longitude, final int locationId, final int likes, final int quotes, final int retweets, final int replies,
	final String tweetDate )
{
	this.tweetPk = tweetPK;
	this.tweetIdStr = tweetIdStr;
	this.content = content;
	this.latitude = latitude;
	this.longitude = longitude;
	this.locationId = locationId;
	this.likes = likes;
	this.quotes = quotes;
	this.retweets = retweets;
	this.replies = replies;
	this.tweetDate = tweetDate;
}

public String getTweetPk( ) { return tweetPk; }

public void setTweetPk( final String tweetPk ) { this.tweetPk = tweetPk; }

public String getTweetIdStr( ) { return tweetIdStr; }

public void setTweetIdStr( final String tweetIdStr ) { this.tweetIdStr = tweetIdStr; }

public String getContent( ) { return content; }

public void setContent( final String content ) { this.content = content; }

public int getLatitude( ) { return latitude; }

public void setLatitude( final int latitude ) { this.latitude = latitude; }

public int getLongitude( ) { return longitude; }

public void setLongitude( final int longitude ) { this.longitude = longitude; }

public int getLocationId( ) { return locationId; }

public void setLocationId( final int locationId ) { this.locationId = locationId; }

public int getLikes( ) { return likes; }

public void setLikes( final int likes ) { this.likes = likes; }

public int getQuotes( ) { return quotes; }

public void setQuotes( final int quotes ) { this.quotes = quotes; }

public int getRetweets( ) { return retweets; }

public void setRetweets( final int retweets ) { this.retweets = retweets; }

public int getReplies( ) { return replies; }

public void setReplies( final int replies ) { this.replies = replies; }

public String getTweetDate( ) { return tweetDate; }

public void setTweetDate( final String tweetDate ) { this.tweetDate = tweetDate; }
}
