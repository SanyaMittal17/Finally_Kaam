window.addEventListener('load',() => {
    const email = localStorage.getItem('email');
    document.getElementById('email').innerHTML = email;
    console.log(email);
})