from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ⚙️ CONFIGURAÇÕES
EMAIL = "Seu EMAIL FIEL"  # 🔹 Substitua pelo seu email do Fiel Torcedor
SENHA = "Sua SENHA FIEL"  # 🔹 Substitua pela sua senha
URL_LOGIN = "https://www.fieltorcedor.com.br/auth/login/"

# 🔥 ABRINDO O NAVEGADOR
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Acessando a página de login
driver.get(URL_LOGIN)

# Espera até os campos de login (email e senha) estarem visíveis
try:
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))  # Espera o campo de email carregar por "name"
    )
    email_field.send_keys(EMAIL)
except Exception as e:
    print(f"Erro ao localizar o campo de email: {e}")

try:
    senha_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))  # Espera o campo de senha carregar por "name"
    )
    senha_field.send_keys(SENHA)
except Exception as e:
    print(f"Erro ao localizar o campo de senha: {e}")

# Agora, o script vai aguardar que você resolva o CAPTCHA manualmente
print("Por favor, resolva o CAPTCHA manualmente e depois pressione Enter para continuar...")
input("Pressione Enter depois de resolver o CAPTCHA...")

# Submeter o formulário de login
senha_field.send_keys(Keys.RETURN)

# Espera um pouco para garantir que o login seja realizado
time.sleep(5)

# Verifica se estamos na página de 'Minha Conta', e redireciona para a página de jogos
current_url = driver.current_url
if "minha-conta" in current_url:
    print("Estamos na página de 'Minha Conta', redirecionando para os jogos...")
    driver.get("https://www.fieltorcedor.com.br/jogos/")
else:
    print("Já estamos na página correta de jogos.")

# Espera até que o botão "COMPRE AGORA" esteja visível na página de jogos
try:
    compra_agora_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'COMPRE AGORA')]"))
    )
    compra_agora_button.click()  # Clica no botão de compra
except Exception as e:
    print(f"Erro ao localizar o botão de 'COMPRE AGORA': {e}")

# Espera carregar a página do jogo
time.sleep(5)

# Verifica a página atual e tenta encontrar o texto "Esgotado" ou o botão de comprar
def verificar_ou_comprar():
    try:
        # Verificar se o texto "Esgotado" está visível na página
        esgotado_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Esgotado')]"))
        )
        print("O ingresso está esgotado!")
        
        # Espera 5 segundos e dá F5 se encontrar o "Esgotado"
        print("Esperando 5 segundos antes de dar F5...")
        time.sleep(5)
        driver.refresh()
        time.sleep(5)  # Espera um pouco antes de tentar novamente
        verificar_ou_comprar()  # Chama novamente a função para verificar

    except Exception as e:
        # Se não estiver esgotado, encontra o botão de comprar
        print(f"Erro ao verificar 'Esgotado': {e}")
        try:
            compra_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'comprar') or contains(text(), 'compre')]"))
            )
            print("Botão de compra encontrado! Clicando...")
            compra_button.click()
        except Exception as e:
            print(f"Erro ao localizar o botão de 'comprar': {e}")
            print("Tentando dar F5 na página...")
            driver.refresh()
            time.sleep(5)
            verificar_ou_comprar()  # Chama novamente a função para tentar de novo

# Chama a função de verificar o status e comprar
verificar_ou_comprar()

# Fechar o navegador após a execução
time.sleep(5)
driver.quit()
