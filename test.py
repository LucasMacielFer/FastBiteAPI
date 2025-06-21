import requests
import json

def fazer_login(url_api, usuario, senha):
    login_url = f"{url_api}/api/login"
    credenciais = {
        "user": usuario,
        "password": senha
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"Enviando requisição POST para: {login_url}")
    print(f"Com os dados: {credenciais}")

    try:
        response = requests.post(login_url, json=credenciais, timeout=10)
        response.raise_for_status()  # Lança uma exceção para códigos de erro (4xx ou 5xx)
        return response.json()

    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP: {errh}")
        if errh.response.status_code == 401:
            print(f"Resposta da API: {errh.response.json()}")
        return None
    except requests.exceptions.ConnectionError as errc:
        print(f"Erro de Conexão: {errc}")
        return None
    except requests.exceptions.Timeout as errt:
        print(f"Erro de Timeout: {errt}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Algo deu errado: {err}")
        return None


API_BASE_URL = "http://127.0.0.1:5000"

print("--- Tentando login com credenciais corretas ---")
resposta_sucesso = fazer_login(API_BASE_URL, "admin", "admin12345")

if resposta_sucesso:
    print("\nAnálise da Resposta (Sucesso):")
    print(f"  Resposta completa: {resposta_sucesso}")
    if resposta_sucesso.get("access"):
        print("  Status: Acesso Concedido!")
        # Aqui você poderia, por exemplo, salvar o token JWT retornado pela API
        # token = resposta_sucesso.get("token")
    else:
        print("  Status: Acesso Negado.")
else:
    print("  Falha ao tentar realizar o login.")

print("\n" + "="*40 + "\n")

print("--- Tentando login com credenciais incorretas ---")
resposta_falha = fazer_login(API_BASE_URL, "admin", "senha_errada")

if resposta_falha:
    print("\nAnálise da Resposta (Falha):")
    print(f"  Resposta completa: {resposta_falha}")
else:
    # A função `fazer_login` já imprime a mensagem de erro detalhada
    print("  Falha ao tentar realizar o login, como esperado.")