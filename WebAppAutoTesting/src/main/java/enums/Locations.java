package enums;

/**
 * list of locations supported by the map visualization
 */
public enum Locations
{
	NEW_YORK("New York", States.NEW_YORK, "2459115"),
	LOS_ANGELES("Los Angeles", States.CALIFORNIA, "2442047"),
	CHICAGO("Chicago", States.ILLINOIS, "2379574"),
	HOUSTON("Houston", States.TEXAS, "2424766"),
	PHOENIX("Phoenix", States.ARIZONA, "2471390"),
	PHILADELPHIA("Philadelphia", States.PENNSYLVANIA, "2471217"),
	SAN_ANTONIO("San Antonio", States.TEXAS, "2487796"),
	DALLAS("Dallas", States.TEXAS, "2388929"),
	SAN_DIEGO("San Diego", States.CALIFORNIA, "2487889"),
	SAN_JOSE("San Jose", States.CALIFORNIA, "2488042"),
	DETROIT("Detroit", States.MICHIGAN, "2391585"),
	SAN_FRANCISCO("San Francisco", States.CALIFORNIA, "2487956"),
	JACKSONVILLE("Jacksonville", States.FLORIDA, "2428344"),
	INDIANAPOLIS("Indianapolis", States.INDIANA, "2427032"),
	AUSTIN("Austin", States.TEXAS, "2357536"),
	COLUMBUS("Columbus", States.OHIO, "2383660"),
	CHARLOTTE("Charlotte", States.NORTH_CAROLINA, "2378426"),
	MEMPHIS("Memphis", States.TENNESSEE, "2449323"),
	BALTIMORE("Baltimore", States.MARYLAND, "2358820"),
	BOSTON("Boston", States.MASSACHUSETTS, "2367105"),
	EL_PASO("El Paso", States.TEXAS, "2397816"),
	MILWAUKEE("Milwaukee", States.WISCONSIN, "2451822"),
	DENVER("Denver", States.COLORADO, "2391279"),
	SEATTLE("Seattle", States.WASHINGTON, "2490383"),
	NASHVILLE("Nashville", States.TENNESSEE, "2457170"),
	WASHINGTON("Washington", States.DISTRICT_OF_COLUMBIA, "2514815"),
	LAS_VEGAS("Las Vegas", States.NEVADA, "2436704"),
	PORTLAND("Portland", States.OREGON, "2475687"),
	LOUISVILLE("Louisville", States.KENTUCKY, "2442327"),
	OKLAHOMA_CITY("Oklahoma City", States.OKLAHOMA, "2464592"),
	TUCSON("Tucson", States.ARIZONA, "2508428"),
	ATLANTA("Atlanta", States.GEORGIA, "2357024"),
	ALBUQUERQUE("Albuquerque", States.NEW_MEXICO, "2352824"),
	KANSAS_CITY("Kansas City", States.MISSOURI, "2430683"),
	FRESNO("Fresno", States.CALIFORNIA, "2407517"),
	SACRAMENTO("Sacramento", States.CALIFORNIA, "2486340"),
	LONG_BEACH("Long Beach", States.CALIFORNIA, "2441472"),
	MESA("Mesa", States.ARIZONA, "2449808"),
	OMAHA("Omaha", States.NEBRASKA, "2465512"),
	CLEVELAND("Cleveland", States.OHIO, "2381475"),
	VIRGINIA_BEACH("Virginia Beach", States.VIRGINIA, "2512636"),
	MIAMI("Miami", States.FLORIDA, "2450022"),
	RALEIGH("Raleigh", States.NORTH_CAROLINA, "2478307"),
	MINNEAPOLIS("Minneapolis", States.MINNESOTA, "2452078"),
	COLORADO_SPRINGS("Colorado Springs", States.COLORADO, "2383489"),
	HONOLULU("Honolulu", States.HAWAII, "2423945"),
	ST_LOUIS("St. Louis", States.MISSOURI, "2486982"),
	TAMPA("Tampa", States.FLORIDA, "2503863"),
	NEW_ORLEANS("New Orleans", States.LOUISIANA, "2458833"),
	CINCINNATI("Cincinnati", States.OHIO, "2380358"),
	PITTSBURGH("Pittsburgh", States.PENNSYLVANIA, "2473224"),
	GREENSBORO("Greensboro", States.NORTH_CAROLINA, "2414469"),
	NORFOLK("Norfolk", States.VIRGINIA, "2460389"),
	ORLANDO("Orlando", States.FLORIDA, "2466256"),
	BIRMINGHAM("Birmingham", States.ALABAMA, "2364559"),
	BATON_ROUGE("Baton Rouge", States.LOUISIANA, "2359991"),
	RICHMOND("Richmond", States.VIRGINIA, "2480894"),
	SALT_LAKE_CITY("Salt Lake City", States.UTAH, "2487610"),
	JACKSON("Jackson", States.MISSISSIPPI, "2428184"),
	TALLAHASSEE("Tallahassee", States.FLORIDA, "2503713"),
	PROVIDENCE("Providence", States.RHODE_ISLAND, "2477058"),
	NEW_HAVEN("New Haven", States.CONNECTICUT, "2458410"),
	//todo finish filling these in
	HARRISBURG("Harrisburg", States.PENNSYLVANIA, "???"),
	USA("???", null, "????"),
	WORLD("???", null, "23424775");

protected String cityName;

protected States state;
protected String woeidStr;

public String getCityName( ) { return cityName; }

public States getState( ) { return state; }

public String getWoeidStr( ) { return woeidStr; }

Locations( final String city, final States state, final String woeid )
{
	this.cityName = city;
	this.state = state;
	this.woeidStr = woeid;
}
}
