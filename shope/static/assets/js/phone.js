const element = document.getElementById('phone');
const maskOptions = {
    mask: '+7(000)000-00-00',
    lazy: false
};
console.log(element)
const mask = IMask(element, maskOptions);