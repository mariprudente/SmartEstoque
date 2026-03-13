$(document).ready(function(){

// CLIENTE
$('#cpf').mask('000.000.000-00');
$('#telefone').mask('(00) 0000-0000');
$('#celular').mask('(00) 00000-0000');

// FORNECEDOR
$('#cnpj').mask('00.000.000/0000-00');
$('#cep').mask('00000-000');
$('#telefone_fornecedor').mask('(00) 0000-0000');
$('#celular_fornecedor').mask('(00) 00000-0000');

});

/* Script das abas de fornecedor*/

function openTab(tabName){

let tabs = document.getElementsByClassName("tabcontent");

for(let i=0;i<tabs.length;i++){

tabs[i].style.display="none";

}

document.getElementById(tabName).style.display="block";

}

function previewImagem(event){

let reader = new FileReader();

reader.onload = function(){

let output = document.getElementById('preview-img');

output.src = reader.result;

}

reader.readAsDataURL(event.target.files[0]);

}