var imagePicker = document.getElementById("image_picker");

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

const token = getCookie("token");

if (token === "") {
    alert("You need to sign in to upload images");
    window.location.href = "/";
}

async function upload_image() {
    const image = imagePicker.files[0];

    const formData = new FormData();
    formData.append("image", image);

    const response = await fetch(`/api/image/upload`, {
        method: "POST",
        headers: { token: token },
        body: formData,
        // Set the FormData instance as the request body
    });

    response_json = await response.json();
    console.log(response_json);
    if (response_json.success === 0) {
        alert(`server returned an error: \n${response_json.error}`);
    } else {
        alert(`successfully uploaded image. Url: ${response_json.url}`);
    }
}
