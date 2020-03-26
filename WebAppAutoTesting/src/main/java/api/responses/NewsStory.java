package api.responses;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * stores information about a new story (which is related to some trend) sent from the backend server
 */
@Data
@NoArgsConstructor
public class NewsStory
{
protected String title;
protected String author;
protected String sourceName;
protected String linkUrl;
protected String date;
protected String description;
protected String contentStart;
}
