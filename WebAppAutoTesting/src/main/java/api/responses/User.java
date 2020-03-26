package api.responses;

import com.google.gson.annotations.SerializedName;

/**
 * stores information about a user sent from the backend server
 */
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

public User( ) { }

public User( final int userPk, final String userId, final String username, final String signupDate,
	final int locationId, final boolean isProtected, final int followersCount, final int friendsCount )
{
	this.userPk = userPk;
	this.userId = userId;
	this.username = username;
	this.signupDate = signupDate;
	this.locationId = locationId;
	this.isProtected = isProtected;
	this.followersCount = followersCount;
	this.friendsCount = friendsCount;
}

public int getUserPk( )
{
	return userPk;
}

public void setUserPk( final int userPk )
{
	this.userPk = userPk;
}

public String getUserId( )
{
	return userId;
}

public void setUserId( final String userId )
{
	this.userId = userId;
}

public String getUsername( )
{
	return username;
}

public void setUsername( final String username )
{
	this.username = username;
}

public String getSignupDate( )
{
	return signupDate;
}

public void setSignupDate( final String signupDate )
{
	this.signupDate = signupDate;
}

public int getLocationId( )
{
	return locationId;
}

public void setLocationId( final int locationId )
{
	this.locationId = locationId;
}

public boolean isProtected( )
{
	return isProtected;
}

public void setProtected( final boolean aProtected )
{
	isProtected = aProtected;
}

public int getFollowersCount( )
{
	return followersCount;
}

public void setFollowersCount( final int followersCount )
{
	this.followersCount = followersCount;
}

public int getFriendsCount( )
{
	return friendsCount;
}

public void setFriendsCount( final int friendsCount )
{
	this.friendsCount = friendsCount;
}
}
