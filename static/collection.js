var visibility = -1;
const makePublicButton = document.getElementById("change_visibility");

const url = window.location.href.split("/");
const collectionID = url[url.length - 1];

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
    const makePublicButton = document.getElementById("change_visibility");

    token = getCookie("token");

    const response = await fetch(`/api/collection/${collectionID}/get_images`, {
        method: "GET",
        headers: { token: token },
        // Set the FormData instance as the request body
    });

    response_json = await response.json();

    // happens if token is invalid
    if (response_json.success === 0) {
        alert(`Server returned an error:\n${response_json.error}`);
        window.location.href = "/";
    }
    for (i = 0; i < response_json.images.length; i++) {
        imageName = response_json.images[i].name;
        imageID = response_json.images[i].id;
        addImageBox(imageID, imageName);
    }

    collectionHeading = document.getElementById("collection_name");
    collectionHeading.textContent = response_json["collectionName"];

    visibility = response_json.public;
    console.log(response_json.public);
    if (visibility === 1) {
        makePublicButton.value = "Click to make this collection private";
    } else {
        makePublicButton.value = "Click to make this collection public";
    }
};

// Function for adding a user to the collection
async function add_user() {
    const userID = document.getElementById("userID_add_user").value;

    token = getCookie("token");

    const formData = new FormData();
    formData.append("userID", userID);

    const response = await fetch(`/api/collection/${collectionID}/add_user`, {
        method: "POST",
        headers: { token: token },
        body: formData,
        // Set the FormData instance as the request body
    });

    response_json = await response.json();

    if (response_json.success === 0) {
        alert(`Server returned an error:\n${response_json.error}`);
    } else {
        alert(`Successfully added user :)`);
    }
}

// function for making the collection public or private
async function change_visibility() {
    if (visibility === 1) {
        visibility = 0;
    } else {
        visibility = 1;
    }
    token = getCookie("token");

    const formData = new FormData();
    formData.append("new_visibility", visibility);

    const response = await fetch(
        `/api/collection/${collectionID}/change_visibility`,
        {
            method: "POST",
            headers: { token: token },
            body: formData,
        }
    );

    response_json = await response.json();

    if (response_json.success === 0) {
        alert(`Server returned an error:\n${response_json.error}`);
    } else {
        if (visibility === 1) {
            makePublicButton.value = "Click to make this collection private";
            alert("Made collection public");
        } else {
            makePublicButton.value = "Click to make this collection public";
            alert("Made collection private");
        }
    }
}

// function for adding an image to the collection
async function add_image() {
    const imageID = document.getElementById("id_add_image").value;

    token = getCookie("token");

    const formData = new FormData();
    formData.append("imageID", imageID);

    const response = await fetch(`/api/collection/${collectionID}/add_image`, {
        method: "POST",
        headers: { token: token },
        body: formData,
        // Set the FormData instance as the request body
    });

    response_json = await response.json();

    if (response_json.success === 0) {
        alert(`Server returned an error:\n${response_json.error}`);
    } else {
        alert(`Successfully added image :)`);
        location.reload();
    }
}
