package base.enums;

/**
 * list of distinct states displayed in the map visualization
 */
public enum States
{
	ALABAMA("Alabama", 0, 0),
	ALASKA("Alaska", 0, 0),
	ARIZONA("Arizona", 0, 0),
	ARKANSAS("Arkansas", 0, 0),
	CALIFORNIA("California", 0.1, 0.2),
	COLORADO("Colorado", 0, 0),
	CONNECTICUT("Connecticut", 0, 0),
	DELAWARE("Delaware", 0, 0),
	//todo deal with the fact that this can never be clicked on for zooming b/c the circles are too big
	DISTRICT_OF_COLUMBIA("District of Columbia", 0, 0),
	FLORIDA("Florida", 0.25, -0.2),
	GEORGIA("Georgia", 0, 0),
	HAWAII("Hawaii", 0.35, 0.3),
	IDAHO("Idaho", 0, 0),
	ILLINOIS("Illinois", 0, 0),
	INDIANA("Indiana", 0, 0),
	IOWA("Iowa", 0, 0),
	KANSAS("Kansas", 0, 0),
	KENTUCKY("Kentucky", 0.15, 0),
	LOUISIANA("Louisiana", -0.15, -0.15),
	MAINE("Maine", 0, 0),
	MARYLAND("Maryland", 0, -0.15),
	MASSACHUSETTS("Massachusetts", 0, 0),
	MICHIGAN("Michigan", 0.2, 0.2),
	MINNESOTA("Minnesota", 0, 0),
	MISSISSIPPI("Mississippi", 0, 0),
	MISSOURI("Missouri", 0, 0),
	MONTANA("Montana", 0, 0),
	NEBRASKA("Nebraska", 0, 0),
	NEVADA("Nevada", 0, 0),
	NEW_HAMPSHIRE("New Hampshire", 0, 0),
	NEW_JERSEY("New Jersey", 0, 0),
	NEW_MEXICO("New Mexico", 0, 0),
	NEW_YORK("New York", 0, 0),
	NORTH_CAROLINA("North Carolina", 0, 0),
	NORTH_DAKOTA("North Dakota", 0, 0),
	OHIO("Ohio", 0, 0),
	OKLAHOMA("Oklahoma", 0, 0),
	OREGON("Oregon", 0, 0),
	PENNSYLVANIA("Pennsylvania", 0, 0),
	RHODE_ISLAND("Rhode Island", 0, 0.2),
	SOUTH_CAROLINA("South Carolina", 0, 0),
	SOUTH_DAKOTA("South Dakota", 0, 0),
	TENNESSEE("Tennessee", 0, 0),
	TEXAS("Texas", 0, 0),
	UTAH("Utah", 0, 0),
	VERMONT("Vermont", 0, 0),
	VIRGINIA("Virginia", 0, 0),
	WASHINGTON("Washington", 0, 0),
	WEST_VIRGINIA("West Virginia", 0, 0),
	WISCONSIN("Wisconsin", 0, 0),
	WYOMING("Wyoming", 0, 0);

protected String stateName;

//for clicking on it; defined relative to the center of the bounding box around the element,
// with positive values going down and right
protected double horizOffsetFraction;
protected double vertOffsetFraction;

States( final String name, final double horizOffset, final double vertOffset )
{
	this.stateName = name;
	this.horizOffsetFraction = horizOffset;
	this.vertOffsetFraction = vertOffset;
}

public String getStateName( ) { return stateName; }

public double getHorizOffsetFraction( ) { return horizOffsetFraction; }

public double getVertOffsetFraction( ) { return vertOffsetFraction; }
}
