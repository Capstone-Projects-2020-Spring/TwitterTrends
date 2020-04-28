package api.responses;

import com.google.gson.annotations.SerializedName;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * stores information about a trend sent from the backend server
 */
@NoArgsConstructor
@Data
public class Trend
{
@SerializedName(value = "trend_PK")
protected int trendPk;

protected String trendContent;
protected boolean isHashtag;
protected String queryTerm;
protected int tweetVolume;
}
