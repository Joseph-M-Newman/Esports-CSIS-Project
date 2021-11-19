"use strict";

$(async ()=> {
    $("#createAccount").click(() =>{createAccount()});
});

async function createAccount(){
var user = $("#u").val();
var pass = $("#p").val();

if(!user){
    $("#uInput").text("Username must not be empty");
    return;
}
let a = new api(user,pass);
let res;
res = await a.add_user();

if(res.err){
    $("#uInput").text(res.err);
}else {
    location.href='/login';
}
}