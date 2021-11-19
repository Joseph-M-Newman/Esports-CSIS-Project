"use strict";
$(async () =>
{
	$("#Login").click(()=> {login()});
});

async function login(){
    var username = $("#user").val();
    var password = $("#pass").val();
    $("#userInput").empty();
    
    if(!username){
        $("#userInput").text("Username must not be empty.")
        return;
    }
    let a = new api(username, password);
    let res;
    console.log(username + " "+ password);
    res = await a.login();


    if(res.err){
        $("#userInput").text(res.err);
    } else {
        sessionStorage.setItem("user",username);
        sessionStorage.setItem("pass",password);
        location.href = "/";
    }
}