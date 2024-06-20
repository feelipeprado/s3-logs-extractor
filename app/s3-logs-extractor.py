import boto3
import os

s3_client = boto3.client('s3')


def download_dir(bucket, prefix, local, client=s3_client):
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
        results = client.list_objects_v2(**kwargs)
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
        client.download_file(bucket, k, dest_pathname)
        print(".", end='')
        cont += 1
    print(f"\n{cont} arquivos baixados")


def main():
    print("Iniciando execução")
    download_dir(bucket, prefix, local)
    print("Finalizando execução")

bucket = "log-bucket-108917090688"  # Bucket que contém os arquivos a serem baixados
base_prefix = "bucket=my-bucket-108917090688"  # Prefixo de arquivos a ser buscado no S3
data_hora_busca = "2024-06-20-03-17" # YYYY-MM-DD-hh-mm-ss
prefix=f"{base_prefix}/{data_hora_busca}"
local = f"logs/{data_hora_busca}"  # Pasta local onde os arquivos serão salvos

main()
