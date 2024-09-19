const forms = document.querySelector(".forms"),
pwShowHide = document.querySelectorAll(".eye-icon"),
links = document.querySelectorAll(".link");

pwShowHide.forEach(eyeIcon => {
eyeIcon.addEventListener("click", () => {
  let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");
  
  pwFields.forEach(password => {
      if(password.type === "password"){
          password.type = "text";
          eyeIcon.classList.replace("bx-hide", "bx-show");
          return;
      }
      password.type = "password";
      eyeIcon.classList.replace("bx-show", "bx-hide");
  })
  
})
})      

links.forEach(link => {
link.addEventListener("click", e => {
 e.preventDefault(); //preventing form submit
 forms.classList.toggle("show-signup");
})
})




    function onSignIn(googleUser) {
        var profile = googleUser.getBasicProfile();
        console.log('ID: ' + profile.getId());
        console.log('Name: ' + profile.getName());
        console.log('Image URL: ' + profile.getImageUrl());
        console.log('Email: ' + profile.getEmail());
        // Aquí puedes enviar la información al servidor o manejar el estado de sesión
    }

    function onSignInFailure(error) {
        console.log('Error during Google Sign-In:', error);
        // Aquí puedes manejar errores de autenticación
    }

    function initGoogleSignIn() {
        gapi.load('auth2', function() {
            gapi.auth2.init().then(function(auth2) {
                var googleSignInButton = document.getElementById('google-signin-button');
                googleSignInButton.addEventListener('click', function() {
                    auth2.signIn().then(onSignIn, onSignInFailure);
                });
            });
        });
    }

    window.onload = initGoogleSignIn;
