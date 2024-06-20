# s3-logs-extractor
Script Python 3.12 para extração de Logs S3 e geração de arquivo XLSX.

## Orientações
Os Logs do S3 são gerados em formato padrão pela AWS para um outro Bucket, onde ficam armazenados e podem ser acessados através de leitura dos arquivos.
A forma recomendada pela AWS é a criação de uma Tabela via Athena que consulta os arquivos e os exibe ao usuário, porém, em alguns casos, a criação da tabela não é possível por travas ou limitações técnicas particulares a conta AWS em questão.

Para estes casos, o Script é uma alternativa para baixar e exportar os logs em formato de tabela numa planilha EXCEL.

### Pré requisitos
1. AWS CLI instalado
2. Python 3.12

### Configurando AWS CLI
1. Tenha uma chave de acesso a sua conta (AWS Access Key ID + AWS Secret Access Key)
2. Execute `aws configure` no terminal e insira as chaves + região + formato de saída desejado (este ultimo sendo opicional)
3. 

### Como Executar
1. Altere no arquivo `s3-logs-extractor.py` as linhas abaixo conforme necessidade:
```python
bucket = "log-bucket-108917090688"  # Bucket que contém os arquivos a serem baixados
base_prefix = "bucket=my-bucket-108917090688"  # Prefixo de arquivos a ser buscado no S3
data_hora_busca = "2024-06-20" # YYYY-MM-DD-hh-mm-ss
```
2. Execute o Script.

> Dica!
> Utilize sempre que possível a variável `data_hora_busca`. Os logs do S3 podem ser volumosos e baixar todos os logs tende a ser muito custoso. Use a variável para limitar a data/hora que deja obter os logs e otimize tanto a execução do seu script quando os custos de Requests no S3.
