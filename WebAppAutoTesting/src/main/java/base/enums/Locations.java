package base.enums;

/**
 * list of locations supported by the map visualization
 */
public enum Locations
{
	NEW_YORK("New York", States.NEW_YORK, "2459115", "40.712776", "-74.005974"),
	LOS_ANGELES("Los Angeles", States.CALIFORNIA, "2442047", "34.052235", "-118.243683"),
	CHICAGO("Chicago", States.ILLINOIS, "2379574", "41.878113", "-87.629799"),
	HOUSTON("Houston", States.TEXAS, "2424766", "29.760427", "-95.369804"),
	PHOENIX("Phoenix", States.ARIZONA, "2471390", "33.448377", "-112.074037"),
	PHILADELPHIA("Philadelphia", States.PENNSYLVANIA, "2471217", "39.952584", "-75.165222"),
	SAN_ANTONIO("San Antonio", States.TEXAS, "2487796", "29.424122", "-98.493628"),
	DALLAS("Dallas", States.TEXAS, "2388929", "32.776664", "-96.796988"),
	SAN_DIEGO("San Diego", States.CALIFORNIA, "2487889", "32.715738", "-117.161084"),
	SAN_JOSE("San Jose", States.CALIFORNIA, "2488042", "37.338208", "-121.886329"),
	DETROIT("Detroit", States.MICHIGAN, "2391585", "42.331427", "-83.045754"),
	SAN_FRANCISCO("San Francisco", States.CALIFORNIA, "2487956", "37.774929", "-122.419416"),
	JACKSONVILLE("Jacksonville", States.FLORIDA, "2428344", "30.332184", "-81.655651"),
	INDIANAPOLIS("Indianapolis", States.INDIANA, "2427032", "39.768403", "-86.158068"),
	AUSTIN("Austin", States.TEXAS, "2357536", "30.267153", "-97.743061"),
	COLUMBUS("Columbus", States.OHIO, "2383660", "39.961176", "-82.998794"),
	CHARLOTTE("Charlotte", States.NORTH_CAROLINA, "2378426", "35.227087", "-80.843127"),
	MEMPHIS("Memphis", States.TENNESSEE, "2449323", "35.149534", "-90.048980"),
	BALTIMORE("Baltimore", States.MARYLAND, "2358820", "39.290385", "-76.612189"),
	BOSTON("Boston", States.MASSACHUSETTS, "2367105", "42.360082", "-71.058880"),
	EL_PASO("El Paso", States.TEXAS, "2397816", "31.777576", "-106.442456"),
	MILWAUKEE("Milwaukee", States.WISCONSIN, "2451822", "43.038902", "-87.906474"),
	DENVER("Denver", States.COLORADO, "2391279", "39.739236", "-104.990251"),
	SEATTLE("Seattle", States.WASHINGTON, "2490383", "47.606209", "-122.332071"),
	NASHVILLE("Nashville", States.TENNESSEE, "2457170", "36.162664", "-86.781602"),
	WASHINGTON("Washington", States.DISTRICT_OF_COLUMBIA, "2514815", "38.907192", "-77.036871"),
	LAS_VEGAS("Las Vegas", States.NEVADA, "2436704", "36.169941", "-115.139830"),
	PORTLAND("Portland", States.OREGON, "2475687", "45.505106", "-122.675026"),
	LOUISVILLE("Louisville", States.KENTUCKY, "2442327", "38.252665", "-85.758456"),
	OKLAHOMA_CITY("Oklahoma City", States.OKLAHOMA, "2464592", "35.467560", "-97.516428"),
	TUCSON("Tucson", States.ARIZONA, "2508428", "32.221743", "-110.926479"),
	ATLANTA("Atlanta", States.GEORGIA, "2357024", "33.748995", "-84.387982"),
	ALBUQUERQUE("Albuquerque", States.NEW_MEXICO, "2352824", "35.085334", "-106.605553"),
	KANSAS_CITY("Kansas City", States.MISSOURI, "2430683", "39.099727", "-94.578567"),
	FRESNO("Fresno", States.CALIFORNIA, "2407517", "36.746842", "-119.772587"),
	SACRAMENTO("Sacramento", States.CALIFORNIA, "2486340", "38.581572", "-121.494400"),
	LONG_BEACH("Long Beach", States.CALIFORNIA, "2441472", "33.770050", "-118.193740"),
	MESA("Mesa", States.ARIZONA, "2449808", "33.415184", "-111.831472"),
	OMAHA("Omaha", States.NEBRASKA, "2465512", "41.252363", "-95.997988"),
	CLEVELAND("Cleveland", States.OHIO, "2381475", "41.499320", "-81.694361"),
	VIRGINIA_BEACH("Virginia Beach", States.VIRGINIA, "2512636", "36.852926", "-75.977985"),
	MIAMI("Miami", States.FLORIDA, "2450022", "25.761680", "-80.191790"),
	RALEIGH("Raleigh", States.NORTH_CAROLINA, "2478307", "35.779590", "-78.638179"),
	MINNEAPOLIS("Minneapolis", States.MINNESOTA, "2452078", "44.977753", "-93.265011"),
	COLORADO_SPRINGS("Colorado Springs", States.COLORADO, "2383489", "38.833882", "-104.821363"),
	HONOLULU("Honolulu", States.HAWAII, "2423945", "21.306944", "-157.858333"),
	ST_LOUIS("St. Louis", States.MISSOURI, "2486982", "38.627003", "-90.199404"),
	TAMPA("Tampa", States.FLORIDA, "2503863", "27.950575", "-82.457178"),
	NEW_ORLEANS("New Orleans", States.LOUISIANA, "2458833", "29.951066", "-90.071532"),
	CINCINNATI("Cincinnati", States.OHIO, "2380358", "39.103118", "-84.512020"),
	PITTSBURGH("Pittsburgh", States.PENNSYLVANIA, "2473224", "40.440625", "-79.995886"),
	GREENSBORO("Greensboro", States.NORTH_CAROLINA, "2414469", "36.072635", "-79.791975"),
	NORFOLK("Norfolk", States.VIRGINIA, "2460389", "36.850769", "-76.285873"),
	ORLANDO("Orlando", States.FLORIDA, "2466256", "28.538335", "-81.379237"),
	BIRMINGHAM("Birmingham", States.ALABAMA, "2364559", "33.520661", "-86.802490"),
	BATON_ROUGE("Baton Rouge", States.LOUISIANA, "2359991", "30.458283", "-91.140320"),
	RICHMOND("Richmond", States.VIRGINIA, "2480894", "37.540725", "-77.436048"),
	SALT_LAKE_CITY("Salt Lake City", States.UTAH, "2487610", "40.760779", "-111.891047"),
	JACKSON("Jackson", States.MISSISSIPPI, "2428184", "32.298757", "-90.184810"),
	TALLAHASSEE("Tallahassee", States.FLORIDA, "2503713", "30.438256", "-84.280733"),
	PROVIDENCE("Providence", States.RHODE_ISLAND, "2477058", "41.823989", "-71.412834"),
	NEW_HAVEN("New Haven", States.CONNECTICUT, "2458410", "41.308274", "-72.927883"),
	HARRISBURG("Harrisburg", States.PENNSYLVANIA, "2418046", "40.273191", "-76.886701"),
	//todo finish filling these in
	USA("???", null, "????", null, null),
	WORLD("???", null, "23424775", null, null);//or woeid = 1?

protected String cityName;

protected States state;
protected String woeidStr;

protected String latitude;
protected String longitude;

public String getCityName( ) { return cityName; }

public States getState( ) { return state; }

public String getWoeidStr( ) { return woeidStr; }

public String getLatitude( ) { return latitude; }

public String getLongitude( ) { return longitude; }

Locations( final String city, final States state, final String woeid, final String latit, final String longit )
{
	this.cityName = city;
	this.state = state;
	this.woeidStr = woeid;
	this.latitude = latit;
	this.longitude = longit;
}
}
