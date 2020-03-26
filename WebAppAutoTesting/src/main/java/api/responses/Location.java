package api.responses;

import com.google.gson.annotations.SerializedName;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * stores information about a location sent from the backend server
 */
@Data
@NoArgsConstructor
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
}
