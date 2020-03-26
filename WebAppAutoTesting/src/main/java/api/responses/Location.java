package api.responses;

import com.google.gson.annotations.SerializedName;

/**
 * stores information about a location sent from the backend server
 */
public class Location
{
@SerializedName(value = "location_PK")
protected int locationPk;

protected String cityId;
protected String stateId;
protected String countryId;
protected int woeid;
protected int latitude;
protected int longitude;

public Location( ) { }

public Location( final int locationPK, final String cityId, final String stateId, final String countryId,
	final int woeid, final int latitude, final int longitude )
{
	this.locationPk = locationPK;
	this.cityId = cityId;
	this.stateId = stateId;
	this.countryId = countryId;
	this.woeid = woeid;
	this.latitude = latitude;
	this.longitude = longitude;
}

public int getLocationPk( )
{
	return locationPk;
}

public void setLocationPk( final int locationPk )
{
	this.locationPk = locationPk;
}

public String getCityId( )
{
	return cityId;
}

public void setCityId( final String cityId )
{
	this.cityId = cityId;
}

public String getStateId( )
{
	return stateId;
}

public void setStateId( final String stateId )
{
	this.stateId = stateId;
}

public String getCountryId( )
{
	return countryId;
}

public void setCountryId( final String countryId )
{
	this.countryId = countryId;
}

public int getWoeid( )
{
	return woeid;
}

public void setWoeid( final int woeid )
{
	this.woeid = woeid;
}

public int getLatitude( )
{
	return latitude;
}

public void setLatitude( final int latitude )
{
	this.latitude = latitude;
}

public int getLongitude( )
{
	return longitude;
}

public void setLongitude( final int longitude )
{
	this.longitude = longitude;
}
}
