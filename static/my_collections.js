function addCollectionLink(collectionID, collectionName) {
    const container = document.getElementById("collection-container");

    // add the text underneath
    const link = document.createElement("a");
    link.textContent = collectionName;
    link.href = `/collection/${collectionID}`;

    // Append the image box to the container
    container.appendChild(link).appendChild(document.createElement("br"));
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
    // happens if no token cookie. cookie monster is sad :(
    if (token === "") {
        alert("You must sign in to access this");
        window.location.href = "/";
    }

    const response = await fetch("/api/user/get_collections", {
        method: "GET",
        headers: { token: token },
    });

    response_json = await response.json();

    // happens if token is invalid
    if (response_json.auth === 0) {
        alert("You must sign in to access this");
        window.location.href = "/";
    }
    console.log(response_json);
    for (i = 0; i < response_json.collections.length; i++) {
        imageName = response_json.collections[i].name;
        imageID = response_json.collections[i].id;
        addCollectionLink(imageID, imageName);
    }
};

async function create_collection() {
    const collectionName = document.getElementById("collection_name").value;

    token = getCookie("token");

    const formData = new FormData();
    formData.append("collectionName", collectionName);

    const response = await fetch(`/api/collection/create`, {
        method: "POST",
        headers: { token: token },
        body: formData,
        // Set the FormData instance as the request body
    });

    console.log(response);

    response_json = await response.json();

    if (response_json.success === 0) {
        alert(`Server returned an error:\n${response_json.error}`);
    } else {
        alert(`Successfully created collection`);
        location.reload;
    }
}
