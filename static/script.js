// Função para alternar entre abas (Tabs)
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}
function confirmarExclusao(id, nome) {
    Swal.fire({
        title: 'Excluir Produto?',
        text: "Você tem certeza que deseja remover '" + nome + "' permanentemente?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33', // Cor vermelha para confirmar
        cancelButtonColor: '#3085d6', // Cor azul para cancelar
        confirmButtonText: 'Sim, excluir!',
        cancelButtonText: 'Cancelar',
        reverseButtons: true // Inverte a ordem para o "Cancelar" ficar na esquerda
    }).then((result) => {
        if (result.isConfirmed) {
            // Se o usuário confirmou, redireciona para a rota de exclusão do Flask
            window.location.href = "/produtos/excluir/" + id;
        }
    })
}
// Máscaras de entrada (Exemplo simples com Regex)
document.addEventListener('DOMContentLoaded', () => {
    const masks = {
        cpf: (value) => value.replace(/\D/g, '').replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4'),
        rg: (value) => value.replace(/\D/g, '').replace(/(\d{2})(\d{3})(\d{3})(\d{1})/, '$1.$2.$3-$4'),
        data: (value) => value.replace(/\D/g, '').replace(/(\d{2})(\d{2})(\d{4})/, '$1/$2/$3'),
        tel: (value) => value.replace(/\D/g, '').replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3'),
        cel: (value) => value.replace(/\D/g, '').replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3'),
        cep: (value) => value.replace(/\D/g, '').replace(/(\d{5})(\d{3})/, '$1-$2'),
        cnpj: (value) => value.replace(/\D/g, '').replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5')
    };

    // Aplica a máscara enquanto o usuário digita
    document.querySelectorAll('[data-mask]').forEach(input => {
        input.addEventListener('input', (e) => {
            const maskType = e.target.getAttribute('data-mask');
            if (masks[maskType]) {
                e.target.value = masks[maskType](e.target.value);
            }
        });
    });
});

<script>
function confirmarExcluirCliente(id, nome) {
    Swal.fire({
        title: 'Remover Cliente?',
        text: "Tem certeza que deseja excluir " + nome + "? Todos os dados vinculados a ele serão perdidos.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sim, excluir!',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/clientes/excluir/" + id;
        }
    })
}
</script>