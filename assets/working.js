function getLocation()
{
    if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(showPosition);
    }
    else
    { 
        alert("Geolocation is not supported by this browser.");
    }
}
function showPosition(position)
{
    window.open("/"+ position.coords.latitude.toString() + "/" + position.coords.longitude.toString() ,name="_self");
}