$(document).ready(function(){
    console.log(sessionStorage.length)
    if(sessionStorage.length > 0){
        username = sessionStorage.getItem("user")
        password = sessionStorage.getItem("pass")
       $("#LOGINB").hide()
       $("#LogOut").show()
    }else {
        $("#LOGINB").show()
        $("#LogOut").hide()
    }

    $("#LogOut").click(() =>	{Logout()});
});


function Logout(){
    sessionStorage.removeItem("user");
    sessionStorage.removeItem("pass");
}