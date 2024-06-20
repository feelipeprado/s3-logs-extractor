import boto3
import os
import pandas as pd

def download_dir(bucket, prefix, local):
    print("Iniciando conexão com S3")
    s3_client = boto3.client('s3')
    print("Iniciando download")
    cont = 0
    keys = []
    dirs = []
    next_token = ''
    base_kwargs = {
        'Bucket': bucket,
        'Prefix': prefix,
    }
    print("Downloading", end='')
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != '':
            kwargs.update({'ContinuationToken': next_token})
        results = s3_client.list_objects_v2(**kwargs)
        contents = results.get('Contents')
        for i in contents:
            k = i.get('Key')
            if k[-1] != '/':
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get('NextContinuationToken')
    for d in dirs:
        dest_pathname = os.path.join(local, d)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(local, k)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        s3_client.download_file(bucket, k, dest_pathname)
        print(".", end='')
        cont += 1
    print("")
    print(f"{cont} arquivos baixados")

def process_logs_directory(directory_path):
    cont=0
    # Lista para armazenar todos os dataframes de logs
    all_logs = []
    # Recursivamente percorre o diretório
    print("Lendo arquivos", end='')
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            cont += 1
            print(".", end='')
            file_path = os.path.join(root, file_name)
            # Lê o arquivo de log
            df = read_s3_logs(file_path)
            # Adiciona ao lista de dataframes
            all_logs.append(df)
    print("")
    print(f"{cont} arquivos lidos")
    # Concatena todos os dataframes em um único dataframe
    combined_df = pd.concat(all_logs, ignore_index=True)
    return combined_df

def read_s3_logs(file_path):
    # Define os nomes das colunas para o formato de log do S3 (W3C Extended Log Format)
    column_names = ['BucketOwner', 'Bucket', 'RequestDateTime', 'RemoteIP', 'Requester',
                    'RequestID', 'Operation', 'Key', 'RequestURI', 'HTTPStatus', 'ErrorCode',
                    'BytesSent', 'ObjectSize', 'TotalTime', 'TurnAroundTime', 'Referrer', 'UserAgent',
                    'VersionId', 'HostId', 'SigV', 'CipherSuite', 'AuthType', 'Endpoint', 'TLSVersion']
    # Leitura do arquivo de log com pandas
    df = pd.read_csv(file_path, delimiter=' ', header=None, names=column_names)#, error_bad_lines=False)
    return df

def export_df_top_excel(df, output_file):
    # Exporta para XLSX
    print("Exportanto para Excel")
    df.to_excel(output_file, index=True, engine='xlsxwriter')
    print(f'Logs exportados para {output_file}')

def main():
    print("Iniciando execução")
    download_dir(bucket, prefix, local)
    df = process_logs_directory(directory_path=local)
    export_df_top_excel(df, output_file=f"{data_hora_busca}-{base_prefix}.xlsx")
    print("Finalizando execução")

bucket = "log-bucket-108917090688"  # Bucket que contém os arquivos a serem baixados
base_prefix = "bucket=my-bucket-108917090688"  # Prefixo de arquivos a ser buscado no S3
data_hora_busca = "2024-06-20" # YYYY-MM-DD-hh-mm-ss
prefix=f"{base_prefix}/{data_hora_busca}"
local = f"logs/{data_hora_busca}"  # Pasta local onde os arquivos serão salvos

main()
