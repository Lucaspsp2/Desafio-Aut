# from appium.webdriver.common.appiumby import AppiumBy

# class MobileLocators:

#     # Tela inicial / abrir app/ fechar banner
#     BANNER_CLOSE = (AppiumBy.ACCESSIBILITY_ID, "Close")
#     OPEN_APP = (AppiumBy.ACCESSIBILITY_ID, "Americanas")
#     ALERT_BUTTON = (AppiumBy.ID, "android:id/button2")

#     # Barra de pesquisa
#     SEARCH_BAR = (AppiumBy.ACCESSIBILITY_ID, "busque aqui seu produto")
#     SEARCH_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(0)')
#     SEARCH_RESULT_ITEM = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.ViewGroup").instance(0)')

#     # Página do produto
#     PRODUCT_NAME = (AppiumBy.ACCESSIBILITY_ID, "Apple iPhone 17 Pro Max 256GB Laranja-cósmico")  # sem click
#     PRODUCT_PRICE = (AppiumBy.ACCESSIBILITY_ID, "R$ 13.498,80")  # sem click
#     ZIP_INPUT = (AppiumBy.ID, "Digite o CEP")
#     CALCULATE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Calcular")
#     DELIVERY_INFO = (AppiumBy.ACCESSIBILITY_ID, "Receba em até 8 dias úteis: Grátis")
#     BUY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("comprar")')

#     # Pop-up Carrinho / Quantidade
#     CART_PRODUCT_CARD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Card Produto")')
#     INCREASE_QTY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Aumentar quantidade em 1")')
#     DECREASE_QTY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Reduzir quantidade em 1")')
#     QUANTITY_FIELD = (AppiumBy.CLASS_NAME, "android.widget.EditText")
#     ADD_CONTINUE = (AppiumBy.ACCESSIBILITY_ID, "adicionar e continuar comprando")

#     # Carrinho final
#     CART_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Carrinho")')
#     CART_COUNT = (AppiumBy.ACCESSIBILITY_ID, "Cesta (2)")  # confirmar quantidade de itens
#     PRODUCT_IN_CART_NAME = (AppiumBy.ACCESSIBILITY_ID, "Apple iPhone 17 Pro Max 256GB Laranja-cósmico")  # sem click
#     PRODUCT_IN_CART_QTY = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("2")')
#     PRODUCT_TOTAL = (AppiumBy.ACCESSIBILITY_ID, "R$ 26.997,60")  # sem click
#     ORDER_TOTAL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "fechar pedido\nR$ 26.997,60")  # sem click

#     # Checkout
#     CHECKOUT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Fechar pedido")')
#     CONTINUE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Continuar")')
#     TERMS_CHECKBOX = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("checkbox")')
#     FINAL_CONTINUE = (AppiumBy.ACCESSIBILITY_ID, "CONTINUAR")
#     EMAIL_CONTINUE_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "Informe seu e-mail para continuar")

from appium.webdriver.common.appiumby import AppiumBy

class MobileLocators:
    # Ícone do App (home do device)
    OPEN_APP_ICON = (AppiumBy.ACCESSIBILITY_ID, "Predicted app: Americanas")

    # Banner promocional (botão fechar)
    BANNER_CLOSE = (AppiumBy.ACCESSIBILITY_ID, "Close")

    # Barra de pesquisa (clicável para habilitar input)
    SEARCH_BAR = (AppiumBy.ACCESSIBILITY_ID, "busque aqui seu produto")
    # "Campo digitável" é o mesmo elemento — enviamos keys para SEARCH_BAR após clicar
    SEARCH_TRIGGER_IMAGE = (AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().className("android.widget.ImageView").instance(0)')

    # Resultado de pesquisa (primeiro item)
    SEARCH_RESULT_ITEM = (AppiumBy.ANDROID_UIAUTOMATOR,
                          'new UiSelector().descriptionStartsWith("Apple iPhone 17 Pro Max 256GB")')
    SEARCH_RESULT_ITEM2 = (AppiumBy.ANDROID_UIAUTOMATOR,
                           'new UiSelector().descriptionContains("Apple Watch se gps")')
    SEARCH_RESULT_ITEM3 = (AppiumBy.ANDROID_UIAUTOMATOR,
                           'new UiSelector().descriptionContains("Apple MacBook Air 13, M3")')

    # Nome dos produtos (xpath específicos que o inspector trouxe)
    PRODUCT_NAME_1 = ('xpath', '//android.view.View[@content-desc="Apple iPhone 17 Pro Max 256GB Prateado"]')
    PRODUCT_NAME_2 = ('xpath', '//android.view.View[@content-desc="Apple Watch se gps Caixa prateada de alumínio – 44 mm Pulseira esportiva denim – p/m"]')
    PRODUCT_NAME_3 = ('xpath', '//android.view.View[@content-desc="Apple MacBook Air 13, M3, cpu de 8 núcleos, gpu de 8 núcleos, 24GB ram, 512GB ssd - Meia-noite"]')

    # Preços dos produtos
    PRODUCT_PRICE_1 = ('xpath', "//android.view.View[contains(@content-desc, '13.498,80')]")
    PRODUCT_PRICE_2 = ('xpath', "//android.view.View[contains(@content-desc, '3.529,00')]")
    PRODUCT_PRICE_3 = ('xpath', "//android.view.View[contains(@content-desc, '18.589,00')]")

    # CEP / entrega
    ZIP_INPUT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Digite o CEP")')
    ZIP_INPUT_BY_RESOURCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Digite o CEP")')  # fallback
    CLEAR_ZIP_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Apagar cep pesquisado")')
    CALCULATE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Calcular")
    ZIP_VALIDATION_TEXT = (AppiumBy.ACCESSIBILITY_ID, "Receba em até 8 dias úteis: Grátis")

    # Comprar/Add
    BUY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("comprar")')
    BUY_NOW = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Comprar agora")')  # inspector
    CARD_PRODUCT = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Card Produto")')
    ADD_CONTINUE = (AppiumBy.ACCESSIBILITY_ID, "adicionar e continuar comprando")

    # Carrinho final / quantidades
    CART_ICON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Carrinho")')
    CART_RESOURCE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Carrinho")')  # sinônimo
    CART_COUNT = (AppiumBy.ACCESSIBILITY_ID, "Cesta")  # texto dinâmico, cheque parcial
    CART_PRODUCT_NAME = (AppiumBy.ACCESSIBILITY_ID, "product_in_cart_name")
    CART_PRODUCT_NAME_XPATH_CONTAINS = ('xpath', "//*[contains(@content-desc, 'Apple iPhone 17 Pro Max 256GB')]")  # exemplo
    INCREASE_QTY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Aumentar quantidade em 1")')
    DECREASE_QTY_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Reduzir quantidade em 1")')
    QUANTITY_FIELD = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    CART_QTY_TEXT_CONTAINS_2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("2")')  # fallback para checar "2"

    # Totais / botão fechar pedido
    PRODUCT_TOTAL = (AppiumBy.ACCESSIBILITY_ID, "product_total")
    ORDER_TOTAL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "fechar pedido")  # texto + valor pode estar no mesmo elemento
    ORDER_TOTAL_BUTTON_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc, 'fechar pedido')]")  # fallback para extrair content-desc com valor

    # Checkout / finalização
    CHECKOUT_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Fechar pedido")')
    CONTINUE_BUTTON = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Continuar")')
    TERMS_CHECKBOX = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("checkbox")')
    FINAL_CONTINUE = (AppiumBy.ACCESSIBILITY_ID, "CONTINUAR")
    EMAIL_CONTINUE_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "Informe seu e-mail para continuar")

    # Modal / Fechar carrinho (se houver)
    CLOSE_CART_MODAL = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Fechar modal carrinho")')
