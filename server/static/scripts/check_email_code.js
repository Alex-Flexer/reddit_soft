window.onload = function () {
    if (!sessionStorage.getItem("email"))
        window.location.replace("/login/")
    else {
        send_code(sessionStorage.getItem("email"))
    }
};

function mark_error(error_message) {
    let error_place = document.getElementById("error_place");
    error_place.innerHTML = error_message;
}

function reset_error() {
    mark_error("");
}

async function confirm_email_code(email, code) {
    const URL = "/confirm/email-code"

    const params = {
        "method": "POST",
        "headers": { "Content-Type": "application/json" },
        "body": JSON.stringify({ "email": email, "code": code })
    };
    try {
        const response = await fetch(URL, params);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const json = await response.json();
        return json;
    }
    catch (error) {
        console.log(error);
        return -1;
    }
}

async function send_code(email) {
    const URL = "/send/email-code/"

    const params = {
        "method": "POST",
        "headers": { "Content-Type": "application/json" },
        "body": JSON.stringify({ "email": email })
    };

    try {
        const response = await fetch(URL, params);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const json = await response.json();
        return json;
    }
    catch (error) {
        console.log(error);
        return -1;
    }
}

async function check_code() {
    let email = sessionStorage.getItem("email");
    reset_error();

    let user_code_element = document.getElementById("user_code")
    let code = user_code_element.value;
    console.log(code);

    if (!code) {
        user_code_element.style.setProperty("--place_holder_color", "red");
        return;
    }

    user_code_element.style.setProperty("--place_holder_color", "#d3dbed");

    let json_user_confirm_code = await confirm_email_code(email, code);
    if (json_user_confirm_code == -1) {
        mark_error("Network Error");
    }
    else if (!json_user_confirm_code["result"]) {
        mark_error(json_user_confirm_code["message"]);
    }
    else {
        localStorage.setItem("email", email);
        window.location.replace("/buy-form/");
    }
}
