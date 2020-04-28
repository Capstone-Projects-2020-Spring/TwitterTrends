package api.responses;

import com.google.gson.annotations.SerializedName;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * stores information about a tweet sent from the backend server
 */
@Data
@NoArgsConstructor
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
}
