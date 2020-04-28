package api.responses;

import com.google.gson.annotations.SerializedName;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * stores information about a user sent from the backend server
 */
@Data
@NoArgsConstructor
public class User
{
@SerializedName(value = "user_PK")
protected int userPk;

protected String userId;
protected String username;
protected String signupDate;
protected int locationId;

@SerializedName(value = "protected")
protected boolean isProtected;

protected int followersCount;
protected int friendsCount;
}
