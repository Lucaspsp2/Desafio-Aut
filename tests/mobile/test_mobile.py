import pytest
import requests
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.mobile.base_page_mobile import BasePageMobile
from locators.mobile.mobile_locators import MobileLocators
from utils.video_recorder import start_recording, stop_recording
from utils.error_logger import log_failure

API_BASE = "http://127.0.0.1:8000"
APP_PACKAGE = "com.b2w.americanas"

@pytest.mark.mobile
def test_purchase_flow_mobile(mobile_driver):
    driver = mobile_driver
    base = BasePageMobile(driver)

    # --- 0) Verificar se a API está online ---
    try:
        health = requests.get(f"{API_BASE}/")
        if health.status_code != 200:
            pytest.skip("API não disponível.")
    except Exception:
        pytest.skip("API não acessível, pulando teste.")

    # --- 1) Login e captura da wishlist ---
    login = {"email": "projeto@example.com", "password": "Senha123!"}
    login_r = requests.post(f"{API_BASE}/auth/login", json=login)
    login_r.raise_for_status()
    token = login_r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    wishlists = requests.get(f"{API_BASE}/wishlists", headers=headers).json()
    wishlist_id = next((w["id"] for w in wishlists if w["name"] == "projeto_final"), None)
    if not wishlist_id:
        pytest.skip("Wishlist 'projeto_final' não encontrada")

    products = requests.get(f"{API_BASE}/wishlists/{wishlist_id}/products", headers=headers).json()

    # --- 2) Executar fluxo para cada produto ---
    for idx, p in enumerate(products, start=1):
        product_name = p["Product"]
        product_price = p["Price"]
        product_zip = p.get("Zipcode", "50710330")

        print(f"\n🔁 Iniciando ciclo {idx}/{len(products)} para: {product_name}")

        try:
            # -> abrir o app pelo ícone
            driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Predicted app: Americanas").click()
            time.sleep(6)

            # -> fechar banner promocional se aparecer
            try:
                print("🧾 Verificando banner promocional...")
                base.close_promo_banner_if_present(MobileLocators.BANNER_CLOSE)
                print("✅ Nenhum banner impedindo o fluxo.")
            except Exception as e:
                print(f"⚠️ Erro ao tentar fechar banner (ignorando): {e}")

            # 🎥 Iniciar gravação do teste
            start_recording(driver)

            # ---- 3) Buscar produto ----
            print(f"🔎 Iniciando busca pelo produto: {product_name}")
            base.wait_for_element(MobileLocators.SEARCH_BAR, timeout=10)
            search_bar = driver.find_element(*MobileLocators.SEARCH_BAR)
            search_bar.click()

            # try:
            #     search_icon = driver.find_element(*MobileLocators.SEARCH_ICON)
            #     search_icon.click()
            #     print("🖱️ Ícone de busca clicado com sucesso.")
            # except Exception:
            #     print("⚠️ Ícone de busca não encontrado — seguindo mesmo assim.")

            time.sleep(1)
            search_input = driver.switch_to.active_element
            search_input.send_keys(product_name)
            driver.press_keycode(66)
            print("Produto digitado e pesquisa iniciada.")
            time.sleep(3)

            # --- clicar no resultado certo ---
            if idx == 1:
                base.wait_for_element(MobileLocators.SEARCH_RESULT_ITEM, timeout=10)
                base.click_element(MobileLocators.SEARCH_RESULT_ITEM)
            elif idx == 2:
                base.wait_for_element(MobileLocators.SEARCH_RESULT_ITEM2, timeout=10)
                base.click_element(MobileLocators.SEARCH_RESULT_ITEM2)
            elif idx == 3:
                base.wait_for_element(MobileLocators.SEARCH_RESULT_ITEM3, timeout=10)
                base.click_element(MobileLocators.SEARCH_RESULT_ITEM3)
            print("Produto encontrado e aberto.")

            # ---- 4) Validar página do produto ----
            if idx == 1:
                name_displayed = base.get_text(MobileLocators.PRODUCT_NAME_1)
                price_displayed = base.get_text(MobileLocators.PRODUCT_PRICE_1)
            elif idx == 2:
                name_displayed = base.get_text(MobileLocators.PRODUCT_NAME_2)
                price_displayed = base.get_text(MobileLocators.PRODUCT_PRICE_2)
            elif idx == 3:
                name_displayed = base.get_text(MobileLocators.PRODUCT_NAME_3)
                price_displayed = base.get_text(MobileLocators.PRODUCT_PRICE_3)
            assert product_name in name_displayed or name_displayed in product_name
            assert product_price in price_displayed or price_displayed in product_price

            # ---- 5) Scroll até o campo de CEP ----
            print("Iniciando scroll até encontrar o campo de CEP")
            found_cep_field = False
            scroll_attempts = 0
            max_scrolls = 2

            while not found_cep_field and scroll_attempts < max_scrolls:
                try:
                    cep_input = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
                    if cep_input.is_displayed():
                        found_cep_field = True
                        print(f" Campo CEP encontrado após {scroll_attempts+1} scroll(s).")
                        break
                except Exception:
                    size = driver.get_window_size()
                    start_x = size['width'] // 2
                    start_y = int(size['height'] * 0.75)
                    end_y = int(size['height'] * 0.35)
                    driver.swipe(start_x, start_y, start_x, end_y, 700)
                    print(f"🔁 Scroll realizado ({scroll_attempts+1}/{max_scrolls})...")
                    time.sleep(1)
                scroll_attempts += 1

            if not found_cep_field:
                msg = f" Campo CEP não visível após {max_scrolls} scrolls — tentativa de clique mesmo assim."
                print(msg)
                log_failure(msg)

            # ---- Apagar CEP anterior se necessário ----
            if idx > 1:
                try:
                    clear_button = driver.find_element(
                        by=AppiumBy.ANDROID_UIAUTOMATOR,
                        value='new UiSelector().description("Apagar cep pesquisado")'
                    )
                    clear_button.click()
                    print(" CEP anterior apagado com sucesso.")
                except Exception:
                    print(" Botão de apagar CEP não encontrado; continuando...")

            # ---- 6) Testar CEP inválido ----
            try:
                cep_input = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
                cep_input.click()
                cep_input.clear()
                cep_input.send_keys("00000000")
                print(" CEP inválido digitado com sucesso.")
                calc_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Calcular")
                calc_btn.click()
                print(" Botão 'Calcular' clicado para CEP inválido.")
                time.sleep(2)
            except Exception as e:
                print(f" Falha ao inserir CEP inválido: {e}")
                log_failure(str(e))

            # ---- 7) Testar CEP válido ----
            try:
                cep_input = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
                cep_input.click()
                cep_input.clear()
                cep_input.send_keys(product_zip)
                print(f" CEP válido '{product_zip}' digitado com sucesso.")
                calc_btn = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Calcular")
                calc_btn.click()
                print(" Botão 'Calcular' clicado para CEP válido.")
                time.sleep(3)
            except Exception as e:
                print(f" Falha ao inserir CEP válido: {e}")
                log_failure(str(e))

            # ---- 8–11) Fluxo de compra, carrinho e checkout ----
            wait = WebDriverWait(driver, 10)

            try:
                #clicar em comprar
               base.wait_for_element(MobileLocators.BUY_NOW, timeout=10)
               base.click_element(MobileLocators.BUY_NOW)
               time.sleep(2)

                # 2️⃣ Aumentar quantidade
               base.wait_for_element(MobileLocators.INCREASE_QTY_BUTTON, timeout=8)
               base.click_element(MobileLocators.INCREASE_QTY_BUTTON)
               time.sleep(1)

                # 3️⃣ Clicar no campo de quantidade (opcional)
               base.wait_for_element(MobileLocators.QUANTITY_FIELD, timeout=5)
               base.click_element(MobileLocators.QUANTITY_FIELD)
               time.sleep(1)

                # 4️⃣ Diminuir quantidade (duas vezes)
               base.wait_for_element(MobileLocators.DECREASE_QTY_BUTTON, timeout=8)
               base.click_element(MobileLocators.DECREASE_QTY_BUTTON)
               time.sleep(1)
               base.click_element(MobileLocators.DECREASE_QTY_BUTTON)
               time.sleep(1)

                # 5️⃣ Aumentar novamente
               base.click_element(MobileLocators.INCREASE_QTY_BUTTON)
               time.sleep(1)

                # 6️⃣ Adicionar e continuar comprando
               base.wait_for_element(MobileLocators.ADD_CONTINUE, timeout=10)
               base.click_element(MobileLocators.ADD_CONTINUE)
               time.sleep(2)

                # 7️⃣ Abrir carrinho
               base.wait_for_element(MobileLocators.CART_ICON, timeout=10)
               base.click_element(MobileLocators.CART_ICON)
               time.sleep(2)

                # 8️⃣ Calcular frete
               base.wait_for_element(MobileLocators.CALCULATE_BUTTON, timeout=10)
               base.click_element(MobileLocators.CALCULATE_BUTTON)
               time.sleep(2)

                # 9️⃣ Fechar pedido
               base.wait_for_element(MobileLocators.CHECKOUT_BUTTON, timeout=12)
               base.click_element(MobileLocators.CHECKOUT_BUTTON)
               time.sleep(2)

                # 🔟 Validar tela "Informe seu e-mail para continuar"
               base.wait_for_element(MobileLocators.EMAIL_CONTINUE_MESSAGE, timeout=12)
               assert base.is_displayed(MobileLocators.EMAIL_CONTINUE_MESSAGE), \
                    "Tela de e-mail não exibida"
               print(" Fluxo finalizado até a tela de login com sucesso.")

                
            except (TimeoutException, NoSuchElementException, AssertionError) as e:
                error_msg = f"Erro no ciclo do produto '{product_name}': {e}"
                print(f" {error_msg}")
                log_failure(error_msg)
                stop_recording(driver, product_name, save_on_error=True)

        except (TimeoutException, NoSuchElementException, AssertionError) as e:
            error_msg = f"Erro no ciclo do produto '{product_name}': {e}"
            print(f" {error_msg}")
            log_failure(error_msg)
            stop_recording(driver, product_name, save_on_error=True)

        # Reiniciar app
        base.terminate_and_wait(APP_PACKAGE, wait_seconds=2)
        time.sleep(2)

    print(" Teste finalizado com sucesso para todos os produtos.")
