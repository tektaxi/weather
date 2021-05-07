const locationSubmit = document.getElementById("location-submit");
locationSubmit.addEventListener("click", onClick);


// gets the user inputted location, not the location we get from the API
function getLocation() {
    const locationInput = document.getElementById("location-value");
    let location = locationInput.value;
    location = location.replace(/\s+/g, '-').toLowerCase();
    return location;
}

function convertTemp(kelvinTemp, unit) {
    if (unit === "f" || "F" || "fahrenheit") {
        let fahrenheitTemp = (((kelvinTemp - 273.15) * 9) / 5) + 32;
        return fahrenheitTemp;
    }
    else if (unit === "c" || "C" || "celsius") {
        let celsiusTemp = kelvinTemp - 273.15;
        return celsiusTemp;
    }
    
}


async function getWeatherData() {
    const location = getLocation();
    const responsedata = (await fetch(`/api/weather-${location}`)).json();
    return responsedata;
}


async function onClick() {
    const data = await getWeatherData();
    // check user settings and add if statement that converts json data to correct system
    // probably should be outside this function but until we have a ui for it i'll just leave it here
    const unitPreference = localStorage.getItem("units");

    const currentData = data["api-return"].current;
    const hourlyData = data["api-return"].hourly;
    const dailyData = data["api-return"].daily;
    const locationData = data["api-return"].location;
    


    document.getElementById("right-now").innerHTML="Right Now";
    
    const location = locationData.display_name;
    document.getElementById("location-name").innerHTML=location;

    const currentWeather = currentData.description;
    // change the description to have proper capitlization
    document.getElementById("current-weather").innerHTML=currentWeather;
    const currentIcon = `https://openweathermap.org/img/wn/${currentData.icon}@2x.png`
    document.getElementById("current-icon").src=currentIcon;
    const currentTemp = `${parseInt(convertTemp(currentData.temp, "fahrenheit"), 10)}°`;   
    document.getElementById("current-temp").innerHTML=currentTemp;
}
