const el_phone = document.getElementById('phone');
const maskOptions = {
    mask: '+7(000)000-00-00',
    lazy: false
};
const mask = IMask(el_phone, maskOptions);

const el_name = document.getElementById("name");
document.getElementById("user-name").textContent = el_name.value;
el_name.oninput = function () {
    document.getElementById("user-name").textContent = el_name.value;
};

document.getElementById("user-phone").textContent = el_phone.value;
el_phone.oninput = function () {
    document.getElementById("user-phone").textContent = el_phone.value;
};

const el_email = document.getElementById("mail");
document.getElementById("user-email").textContent = el_email.value;


function deliveryChange(src) {
    document.getElementById("order-delivery").textContent = src.value
}

function payChange(src) {
    document.getElementById("order-pay").textContent = src.value
}

const el_city = document.getElementById("city");
el_city.oninput = function () {
    document.getElementById("order-city").textContent = el_city.value;
};

const el_address = document.getElementById("address");
el_address.oninput = function () {
    document.getElementById("order-address").textContent = el_address.value;
};
