function initMap() {

    const loc = { lat: 14.857387784410587, lng: 120.81410071852738 };

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: loc,
    });

    const marker = new google.maps.Marker({
        position: loc,
        map: map,
    });
}