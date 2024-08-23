function addImageBox(imageID, imageName) {
    const container = document.getElementById("image-container");

    // make a box for the image
    const imageBox = document.createElement("div");
    imageBox.className = "image-box";

    // add the image to the box
    const img = document.createElement("img");
    img.src = `/api/image/thumbnail/${imageID}`;
    img.alt = imageName;
    imageBox.appendChild(img);

    // add the text underneath
    const link = document.createElement("a");
    link.textContent = imageName;
    link.href = `/image/${imageID}`;
    link.target = "_blank"; // makes the link open in new tab

    imageBox.appendChild(link);

    // Append the image box to the container
    container.appendChild(imageBox);
}

// cookie function from w3 schools
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(";");
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == " ") {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// Example: Adding a few images on page load
window.onload = async function () {
    token = getCookie("token");
    console.log(token);
    // happens if no token cookie. cookie monster is sad :(
    if (token === "") {
        alert("You must sign in to access this");
        window.location.href = "/";
    }

    const response = await fetch("/api/user/get_images", {
        method: "GET",
        headers: { token: token },
        // Set the FormData instance as the request body
    });

    response_json = await response.json();

    // happens if token is invalid
    if (response_json.auth === 0) {
        alert("You must sign in to access this");
        window.location.href = "/";
    }
    for (i = 0; i < response_json.images.length; i++) {
        imageName = response_json.images[i].name;
        imageID = response_json.images[i].id;
        addImageBox(imageID, imageName);
    }
    addImageBox(1, "abc");
    addImageBox(2, "abc");
    addImageBox(3, "abc");
    addImageBox(4, "abc");
};

// token = getCookie("token");
// if (token === "") {
//     console.log("asdjklasdhasjd");
//     // send user back
// }
// var xmlHttp = new XMLHttpRequest();
// xmlHttp.open("GET", "/api/user/get_images");
// xhr.setRequestHeader("token", token);
// xmlHttp.send(null);

// console.log(xmlHttp.responseText);
// // return xmlHttp.responseText;
