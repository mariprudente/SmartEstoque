import os
import datetime

# CONFIGURAÇÕES DO SEU BANCO
DB_USER = "root"
DB_PASSWORD = "PISmartEstoque@2026"  # Aqui usamos a senha normal, sem o %40
DB_NAME = "smartestoque"
BACKUP_PATH = "backups/"

# Criar a pasta de backup se não existir
if not os.path.exists(BACKUP_PATH):
    os.makedirs(BACKUP_PATH)

# Nome do arquivo com data e hora
data_atual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
arquivo_saida = f"{BACKUP_PATH}backup_{DB_NAME}_{data_atual}.sql"

# Comando do MySQL para exportar (mysqldump)
# Nota: O caminho abaixo pode variar conforme sua instalação
comando = f'"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump" -u {DB_USER} -p{DB_PASSWORD} {DB_NAME} > {arquivo_saida}'

print(f"Iniciando backup de {DB_NAME}...")
try:
    os.system(comando)
    print(f"✅ Backup concluído com sucesso: {arquivo_saida}")
except Exception as e:
    print(f"❌ Erro ao realizar backup: {e}")