var crypto_token = null;

window.onload = async function () {
    let email = null;
    if (!localStorage.getItem("email")) {
        window.location.replace("/login");
        return;
    }
    email = localStorage.getItem("email");
    document.querySelector(".section:nth-child(1) > h2:nth-child(2)").innerHTML = email;
    
    json_crypto_token = await get_crypto_token();
    if (json_crypto_token == -1) {
        mark_error("Network error");
    }
    else if (!json_crypto_token["result"]) {
        mark_error(json_crypto_token["message"]);
    }
    else {
        crypto_token = json_crypto_token["token"];
        set_price(email);
    }
}

async function get_crypto_token() {
    const URL = "/get/crypto-token/";

    const params = {
        "method": "GET",
        "headers": { "Content-Type": "application/json" },
    };
    try {
        let response = await fetch(URL, params);
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

function copy_token() {
    if (crypto_token) {
        navigator.clipboard.writeText(crypto_token)
            .catch(err => {
                console.error("Failed to copy text: ", err);
            });
    }
}

function mark_error(error_message) {
    let error_place = document.getElementById("error_place");
    error_place.innerHTML = error_message;
}

function reset_error() {
    mark_error("");
}

async function get_user_price(email, price) {
    const URL = "/get/price/"

    const params = {
        "method": "POST",
        "headers": { "Content-Type": "application/json" },
        "body": JSON.stringify({ "email": email, "price": price })
    };
    try {
        let response = await fetch(URL, params);
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

async function check_user_transaction(email) {
    const URL = "/check/transaction/"

    const params = {
        "method": "POST",
        "headers": { "Content-Type": "application/json" },
        "body": JSON.stringify({ "email": email })
    };
    try {
        let response = await fetch(URL, params);
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



async function set_price(email) {
    let price_element = document.getElementById("price");
    let json_price = await get_user_price(email, 300);
    if (json_price == -1) {
        mark_error("Network error");
    }
    else if (!json_price["result"]) {
        mark_error(json_price["message"]);
    }
    else {
        price_element.innerHTML = json_price["price"];
    }
}

async function check_transaction() {
    let b1 = document.querySelector(".continue_button");
    let b2 = document.querySelector(".alternative_button");

    b1.classList.add("unavailable");
    b2.classList.add("unavailable");

    let email = sessionStorage.getItem("email");
    json_checking_transaction = await check_user_transaction(email);

    if (json_checking_transaction == -1) {
        mark_error("Network error");
    }
    else if (!json_checking_transaction["result"]) {
        mark_error(json_checking_transaction["message"]);
    }
    else {
        sessionStorage.setItem("purchase", true);
        window.location.replace("/successful-purchase");
    }

    b1.classList.remove("unavailable");
    b2.classList.remove("unavailable");
}