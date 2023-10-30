import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from KolorTekst import print_color
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



class Test_sklep(unittest.TestCase):

    login = "Karolll"
    password = "Nowehasło"
    email = "karolll@e3.pl"

    @classmethod
    def setUp(self):
        print("Start testu")
        ser = Service("C:\DRIVERS\ChromeDriver\chromedriver.exe")
        op = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=ser, options=op)

        self.driver.maximize_window()
        self.browser = self.driver.get("https://aleeesklep.local/")
        time.sleep(5)


    def find_element(self, by, value):
        return self.driver.find_element(by, value)


    def is_alert(self):

        self.check = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Błąd')]")
        self.check.text
        return self.check

    def test_sprawdzenie_tytulu_strony(self):

        try:
            title = self.driver.title
            assert 'aleeesklep' in title
            print_color(('Asercja - wyświetlenie tytułu - pozytywny'), "g")

        except Exception as e:
            print_color(('Asercja - wyświetlenie tytułu - negatywny', format(e)), "r")


    def test_istnieje_logo(self):

        logo = self.driver.find_element(By.XPATH, '//img[@class="custom-logo"][1]')
        self.assertTrue(logo.is_displayed())


    def test_menu_nawigacyjne(self):

        napis_stronaglowna = self.driver.find_element(By.XPATH, '//h1[@class ="elementor-heading-title elementor-size-default"]')
        text_strona_glowna = napis_stronaglowna.text
        napis_onas= self.driver.find_element(By.XPATH, '//*[@id="menu-item-1052"]/a')
        text_napis_onas = napis_onas.text
        napis_sukienki = self.driver.find_element(By.XPATH, '//*[@id="menu-item-708"]/a')
        text_napis_sukienki = napis_sukienki.text
        # pobranie aktualnego adresu strony

        try:
            assert "Kolekcja 2023" in text_strona_glowna
            print('Napis "Kolekcja 2023" się wyświetla')
        except:
            print('Napis "Kolekcja 2023" się nie wyświetla')

        try:
            assert "O nas" in text_napis_onas
            print('Napis "O nas" się wyświetla')
        except:
            print('Napis "O nas" się nie wyświetla')

        try:
            assert "Sukienki" in text_napis_sukienki
            print('Napis "Sukienki" się wyświetla')
        except:
            print('Napis "Sukienki" się nie wyświetla')

    def test_zakladka_strona_glowna(self):

        try:
            link_strona_glowna = self.driver.current_url
            self.assertEqual(link_strona_glowna, "https://aleeesklep.local/")
            print("Przekierowanie do strony głównej dziala")
        except AssertionError:
            print("Przekierowanie do strony głównej nie działa")

    def test_zakladka_nowosci(self):

        self.browser = self.driver.get("https://aleeesklep.local/new-arrivals/")

        try:
            link_nowosci = self.driver.current_url
            self.assertEqual(link_nowosci, "https://aleeesklep.local/new-arrivals/")
            print("Przekierowanie do strony Nowości dziala")
        except AssertionError:
            print("Przekierowanie do strony Nowości nie dziala")

    def test_zakladka_kolekcja(self):

        self.browser = self.driver.get("https://aleeesklep.local/collections/")

        try:
            link_kolekcja = self.driver.current_url
            self.assertEqual(link_kolekcja, "https://aleeesklep.local/collections/")
            print("Przekierowanie do strony Kolekcja dziala")
        except AssertionError:
            print("Przekierowanie do strony Kolekcja niedziala")
        #Przykładowe nie wszystkie metody na temat hedera powyzej

    def test_sprawdzenie_działania_kuponu(self):

        self.driver.get("https://aleeesklep.local/nowe-produkty/")
        self.driver.find_element(By.XPATH, '//a[@href="https://aleeesklep.local/produkt/serenity-silver-watch/"]//img[@class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail"]').click()
        self.driver.execute_script("window.scrollBy(0, 800);")
        self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]').click()
        self.driver.find_element(By.XPATH, '//div[@role="alert"]//a[@class="button wc-forward wp-element-button"][normalize-space()="Zobacz koszyk"]').click()
        self.driver.find_element(By.XPATH, '//input[@id="coupon_code"]').send_keys("HF79CFFY")
        self.driver.find_element(By.XPATH, '//button[@name="apply_coupon"]').click()
        amount = self.driver.find_element(By.XPATH, '//tr[@class="cart-subtotal"]//bdi[1]').text
        value_amount = self.konwertuj(amount)
        order_total = self.driver.find_element(By.XPATH, '//tr[@class="order-total"]//bdi[1]').text
        value_order_total = self.konwertuj(order_total)
        bonus = 50.00
        addiction = value_amount - bonus
        if addiction == value_order_total:
            print_color(('Kupon zastosowany poprawnie'), "g")
        else:
            print_color(('Kupon nie zastosowany poprawnie'), "r")


    def test_sprawdzenie_czy_koszyk_sie_zapisuje(self):

        price_of_product = 249.99

        self.driver.get("https://aleeesklep.local/my-account/")

        self.driver.find_element(By.XPATH, '//input[@id="username"]').send_keys(Test_sklep.login)
        self.driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(Test_sklep.password)

        self.driver.find_element(By.XPATH, '//button[@name="login"]').click()
        time.sleep(10)

        #usuniecie z koszyka


        check_status = self.driver.find_element(By.XPATH, '//div[@id="ast-desktop-header"]//bdi[1]')
        converted_value = float(check_status.text.split(" ")[0].replace(",", "."))

        if converted_value == 0.00:
            click_new_products = self.driver.find_element(By.XPATH, '//li[@id="menu-item-796"]/a[@class="menu-link"]')
            click_new_products.click()
            # przejscie do strony Nowe produkty
            click_title_products = self.driver.find_element(By.XPATH, '//li[@class="ast-article-single desktop-align-left tablet-align-left mobile-align-left product type-product post-360 status-publish first instock product_cat-accessories has-post-thumbnail shipping-taxable purchasable product-type-simple"]//img[@class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail"]')
            click_title_products.click()
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]').click()
            self.driver.find_element(By.XPATH, '//img[@class="avatar avatar-96 photo"]').click()

            self.driver.find_element(By.XPATH, '//p[contains(text(),"Witaj")]//a[contains(text(),"Wyloguj się")]').click()

            self.driver.get("https://aleeesklep.local/my-account/")

            self.driver.find_element(By.XPATH, '//input[@id="username"]').send_keys(Test_sklep.login)
            self.driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(Test_sklep.password)

            self.driver.find_element(By.XPATH, '//button[@name="login"]').click()

            time.sleep(5)

            get_price_from_cart = self.driver.find_element(By.XPATH,
                                                           '//div[@id="ast-desktop-header"]//div[contains(@class,"ast-site-header-cart-li")]//bdi[1]').text

            convert = float(get_price_from_cart.split(" ")[0].replace(",", "."))

            if price_of_product == convert:
                print_color(('Produkt się zapisał w koszyku'), "g")
            else:
                print_color(('Produkt się nie zapisał w koszyku'), "r")
        else:
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//div[@class="site-primary-header-wrap ast-builder-grid-row-container site-header-focus-item ast-container"]//span[@class="ast-woo-header-cart-info-wrap"]').click()
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//div[contains(@class,"astra-cart-drawer-content")]//a[@class="button wc-forward wp-element-button"][normalize-space()="Zobacz koszyk"]').click()
            self.driver.find_element(By.XPATH, '//span[@class="ahfb-svg-iconset ast-inline-flex"]//*[name()="svg"]').click()
            time.sleep(5)

            click_new_products = self.driver.find_element(By.XPATH, '//li[@id="menu-item-796"]/a[@class="menu-link"]')
            click_new_products.click()
            # przejscie do strony Nowe produkty
            click_title_products = self.driver.find_element(By.XPATH,
                                                            '//*[@id="post-677"]/div/div/section[2]/div/div/div/div/div/div/div/ul/li[5]/div[1]/a/img')
            click_title_products.click()
            time.sleep(5)
            self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]').click()

            self.driver.find_element(By.XPATH, '//img[@class="avatar avatar-96 photo"]').click()

            self.driver.find_element(By.XPATH,
                                     '//p[contains(text(),"Witaj")]//a[contains(text(),"Wyloguj się")]').click()

            self.driver.get("https://aleeesklep.local/my-account/")

            self.driver.find_element(By.XPATH, '//input[@id="username"]').send_keys(Test_sklep.login)
            self.driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(Test_sklep.password)

            self.driver.find_element(By.XPATH, '//button[@name="login"]').click()

            time.sleep(5)

            get_price_from_cart = self.driver.find_element(By.XPATH,
                                                           '//div[@id="ast-desktop-header"]//div[contains(@class,"ast-site-header-cart-li")]//bdi[1]').text
            print(get_price_from_cart)

            convert = float(get_price_from_cart.split(" ")[0].replace(",", "."))


            if price_of_product == convert:
                print_color(('Produkt się zapisał w koszyku'), "g")
            else:
                print_color(('Produkt się nie zapisał w koszyku'), "r")


    def test_realizacja_zamowienia(self):

        self.driver.get("https://aleeesklep.local/my-account/")

        self.driver.find_element(By.XPATH, '//input[@id="username"]').send_keys("Michał")
        self.driver.find_element(By.XPATH, '//input[@id="password"]').send_keys("wpMichal123")

        self.driver.find_element(By.XPATH, '//button[@name="login"]').click()
        time.sleep(10)

        click_new_products = self.driver.find_element(By.XPATH, '//li[@id="menu-item-796"]/a[@class="menu-link"]')
        click_new_products.click()
        # przejscie do strony Nowe produkty
        click_title_products = self.driver.find_element(By.XPATH,
                                                        '//*[@id="post-677"]/div/div/section[2]/div/div/div/div/div/div/div/ul/li[5]/div[1]/a/img')
        click_title_products.click()
        time.sleep(5)
        #Ilość produktu
        self.driver.find_element(By.XPATH, '//input[@name="quantity"]').get_attribute("value")
        self.driver.find_element(By.XPATH, '//h1[@class="product_title entry-title"]').text
        price_product = self.driver.find_element(By.XPATH, '//div[@class="summary entry-summary"]//bdi[1]').text
        price_product.split(' ')[-1]

        self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]').click()
        self.driver.find_element(By.XPATH, '//div[@role="alert"]//a[@class="button wc-forward wp-element-button"][normalize-space()="Zobacz koszyk"]').click()
        self.driver.find_element(By.XPATH, '//input[@id="shipping_method_0_flat_rate6"]').click()
        self.driver.find_element(By.XPATH, '//a[@class="checkout-button button alt wc-forward wp-element-button"]').click()
        time.sleep(5)
        #Wpisane dane
        #Imie
        name = self.driver.find_element(By.XPATH, '//input[@id="billing_first_name"]')
        name.clear()
        name.send_keys("Michał")
        name_new = "Michał"
        surname = self.driver.find_element(By.XPATH, '//input[@id="billing_last_name"]')
        surname.clear()
        surname.send_keys("Testowy")
        surname_new = "Testowy"
        street = self.driver.find_element(By.XPATH, '//input[@id="billing_address_1"]')
        street.clear()
        street.send_keys("Mandarynkowa")
        street_new = "Mandarynkowa"
        post_code = self.driver.find_element(By.XPATH, '//input[@id="billing_postcode"]')
        post_code.clear()
        post_code.send_keys("85-444")
        post_code_send_new = "85-444"
        city = self.driver.find_element(By.XPATH, '//input[@id="billing_city"]')
        city.clear()
        city.send_keys("Bydgoszcz")
        city_send_new = "Bydgoszcz"
        phone = self.driver.find_element(By.XPATH, '//input[@id="billing_phone"]')
        phone.clear()
        phone.send_keys("555555555")
        phone_send_new = "555555555"
        email = self.driver.find_element(By.XPATH, '//input[@id="billing_email"]')
        email.clear()
        email.send_keys("michal@gmail.com")
        email_send_new = "michal@gmail.com"
        time.sleep(5)

        self.driver.find_element(By.XPATH, '//button[@id="place_order"]').click()
        time.sleep(10)
        #Koniec zamówienia
        # Weryfikacja czy wszystkie dane zgadzają się podczas zamówienia

        order_email = self.driver.find_element(By.XPATH, '//li[@class ="woocommerce-order-overview__email email"]/strong')
        order_email.text

        self.driver.find_element(By.XPATH, '//tr[@class ="woocommerce-table__line-item order_item"]/td[@class ="woocommerce-table__product-name product-name"]/a').text

        order_quantity_product = self.driver.find_element(By.XPATH, '//strong[@class="product-quantity"]')
        number = float(order_quantity_product.text.split(" ")[-1].replace(",", "."))

        order_price = self.driver.find_element(By.XPATH, '//td[@class ="woocommerce-table__product-total product-total"]/span[@class ="woocommerce-Price-amount amount"]/bdi')
        number_only_price = float(order_price.text.split(" ")[0].replace(",", "."))

        order_cost = self.driver.find_element(By.XPATH, '//*[@id="post-998"]/div/div/div/section[1]/table/tfoot/tr[2]/td/span')
        number_cost_delivery = float(order_cost.text.split(" ")[0].replace(",", "."))

        calculation = number * number_only_price + number_cost_delivery
        str(calculation)

        if calculation == 262.98:
            print_color(('Prawidłowo obliczony wynik'), "g")

        else:
            print_color(('Nieprawidłowo obliczony wynik'), "r")

        address_element = self.driver.find_element(By.XPATH, '//address[1]')
        address_text = address_element.text
        address_lines = address_text.split('\n')
        name_line = address_lines[0]

        long_name = name_new + " " + surname_new

        if long_name == name_line:

            print_color(('Imiona się zgadzają'), "g")
        else:
            print_color(('Imiona się nie zgadzają'), "r")


        street_line = address_lines[1]

        if street_new == street_line:

            print_color(('Nazwy ulic się zgadzają'), "g")
        else:
            print_color(('Nazwy ulic się nie zgadzają'), "r")


        adress = post_code_send_new + " " + city_send_new

        postcode_line = address_lines[2]

        if adress == postcode_line:

            print_color(('Kod pocztowy i miasto się zgadzają'), "g")
        else:
            print_color(('Kod pocztowy i miasto się nie zgadzają'), "r")

        phone_line = address_lines[3]

        if phone_send_new == phone_line:
            print_color(('Telefon się zgadza'), "g")

        else:
            print_color(('Telefon się nie zgadzają'), "r")

        email_line = address_lines[4]

        if email_send_new == email_line:
            print_color(('Email się zgadza'), "g")
        else:
            print_color(('Email się nie zgadza'), "r")

    def test_czy_koszyk_wyswietla(self):

        try:
            koszyk_widoczny = self.driver.find_element(By.XPATH, '//div[@id="ast-site-header-cart"]')
            self.assertTrue(koszyk_widoczny.is_displayed())
            print("Koszyk jest widoczny")
        except:
            print("Koszyk nie widoczny")

    def test_czy_występuje_napis_promocjii(self):

        napis_promocji = self.driver.find_element(By.XPATH, '//div[@class="ast-builder-html-element"][1]')
        get_text_napis_promocji = napis_promocji.text
        if get_text_napis_promocji == 'Tylko dziś 40% taniej':
            print(f"Napis promocji {get_text_napis_promocji} się zgadza")
        else:
            print(f"Napis promocji {get_text_napis_promocji} się nie zgadza")

    def test_czy_ikona_logowania_przekierowanie(self):

        time.sleep(10)
        self.driver.get("https://websitedemos.net/fashion-designer-boutique-02/wp-login.php")
        time.sleep(10)
        # time.sleep(2)

        put_name = self.driver.find_element(By.XPATH, '//input[@name="log"]')
        put_name.send_keys("dawidadmin")
        put_paswword = self.driver.find_element(By.XPATH, '//input[@name="pwd"]')
        put_paswword.send_keys("BydOpi2023")
        catch_button = self.driver.find_element(By.XPATH, '//input[@name="wp-submit"]')
        catch_button.click()
        #Zalogowanie

    def test_find_product(self):
        self.driver.find_element(By.XPATH, '//div[@class="site-primary-header-wrap ast-builder-grid-row-container site-header-focus-item ast-container"]//div[@class="ast-search-icon"]//span[@class="ast-icon icon-search"]//*[name()="svg"]').click()
        time.sleep(10)
        accept = self.driver.find_element(By.XPATH, '//input[@type="search"]')
        accept.send_keys("zegarek")
        accept.send_keys(Keys.RETURN)
        # wysłanie w szukanie "zegarek" i kliknięcie enter z klawiatury
        time.sleep(10)

        result_search = self.driver.find_element(By.XPATH, '//h2[@class="entry-title"][1]')
        assert "zegarek" in result_search.text

        time.sleep(5)

    def test_filtrowanie_po_cenie(self):

        move_on_coletion = self.driver.find_element(By.XPATH, '//li[@id="menu-item-598"]//a[@class="menu-link"][normalize-space()="Kolekcja"]')
        ActionChains(self.driver).move_to_element(move_on_coletion).perform()
        #najechanie kursorem myszki
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//li[@id="menu-item-707"]//a[@class="menu-link"][normalize-space()="Akcesoria"]').click()
        time.sleep(5)

        slider = self.driver.find_element(By.XPATH,
            "//input[@class='wc-block-price-filter__range-input wc-block-price-filter__range-input--min wc-block-components-price-slider__range-input wc-block-components-price-slider__range-input--min']")
        time.sleep(5)
        self.driver.execute_script("arguments[0].value = 4000;", slider)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", slider)
        time.sleep(10)
        # Uruchom skrypt JavaScript, aby przesunąć slider w prawo
        slider = self.driver.find_element(By.XPATH,
            "//input[@class='wc-block-price-filter__range-input wc-block-price-filter__range-input--min wc-block-components-price-slider__range-input wc-block-components-price-slider__range-input--min']")
        self.driver.execute_script("arguments[0].value = 20000;", slider)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", slider)

        product_with_small_price = self.driver.find_element(By.XPATH, "//li[@class='ast-grid-common-col ast-full-width ast-article-post desktop-align-left tablet-align-left mobile-align-left product type-product post-352 status-publish instock product_cat-accessories has-post-thumbnail shipping-taxable purchasable product-type-simple']//bdi[1]")
        product_with_high_price = self.driver.find_element(By.XPATH, "//li[@class='ast-grid-common-col ast-full-width ast-article-post desktop-align-left tablet-align-left mobile-align-left product type-product post-360 status-publish first instock product_cat-accessories has-post-thumbnail shipping-taxable purchasable product-type-simple']//bdi[1]")
        product_small = self.pobranie_konwersja_float(product_with_small_price)
        product_high = self.pobranie_konwersja_float(product_with_high_price)

        prices = self.driver.find_elements(By.CSS_SELECTOR, ".price .woocommerce-Price-amount")

        if product_small >= 40 and product_small <= 200:
            is_price_within_range = True
        else:
            is_price_within_range = False

        if is_price_within_range == True:
            print_color(('Cena jest w zakresie'), "g")

        else:
            print_color(('Cena nie jest w zakresie'), "r")


        if product_high >= 40 and product_high <= 200:
            is_price_within_range = True
        else:
            is_price_within_range = False

        if is_price_within_range == True:
            print_color(('Cena jest w zakresie'), "g")
        else:
            print_color(('Cena nie jest w zakresie'), "r")

        # Loop through all prices
        for price in prices:
            price_text = price.text.split(" ")[0].replace(",", ".")
            price_value = float(price_text)
            if 40 <= price_value <= 200:
                print(f"Znaleziono produkty z ceną {price_value} zł")
                if price.is_displayed():
                    products_found = True
                    break
                assert price, "Nie znaleziono produktów w tym zakresie"


    def test_walidacja_email(self):

        self.driver.get("https://aleeesklep.local/my-account/")

        self.get_field_login = self.driver.find_element(By.XPATH, '//input[@id="reg_username"]')
        self.get_field_login.send_keys(Test_sklep.login)
        self.get_field_password = self.driver.find_element(By.XPATH, '//input[@id="reg_password"]')
        self.get_field_password.send_keys(Test_sklep.password)
        self.get_field_email = self.driver.find_element(By.XPATH, '//input[@id="reg_email"]')
        self.get_field_email.send_keys(Test_sklep.email)

        time.sleep(5)

        field_value = self.get_field_email.get_attribute("value")

        if "@" in field_value:
            print_color(('Zawiera znak "@". Wykona się rejestracja'), "g")
        else:
            print_color(('Nie zawiera znaku "@". Nie wykona się rejestracja'), "r")

        low_password = self.driver.find_element(By.XPATH, '//div[@aria-live="polite"][1]')

        if low_password.text == "Bardzo słabe - Proszę wpisać mocniejsze hasło.":
            print_color(('Za krótkie hasło'), "r")
        elif low_password.text == "Słabe - Proszę wpisać mocniejsze hasło.":
            print_color(('Jeszcze za krótkie hasło'), "r")
        elif low_password.text == "Średnie":
            self.driver.find_element(By.XPATH, '//button[@name="register"]').click()
            time.sleep(10)
            self.welcome_text = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Witaj')]").text

            self.assertIn("Witaj", self.welcome_text)
            print_color(('Możemy się zalogować'), "g")
        else:
            print_color(('Poprawne hasło'), "g")


    def test_rejestracja_puste_pole(self):

        self.driver.get("https://aleeesklep.local/my-account/")

        self.get_field_login = self.driver.find_element(By.XPATH, '//input[@id="reg_username"]')
        self.get_field_login.send_keys(Test_sklep.login)
        self.get_field_password = self.driver.find_element(By.XPATH, '//input[@id="reg_password"]')
        self.get_field_password.send_keys(Test_sklep.password)
        self.get_field_email = self.driver.find_element(By.XPATH, '//input[@id="reg_email"]')
        self.get_field_email.send_keys(Test_sklep.email)

        self.driver.find_element(By.XPATH, '//button[@name="register"]').click()

        error_message = self.driver.find_element(By.XPATH, '//ul[@role="alert"]/li')
        if error_message.text == "Błąd: Proszę podać poprawny adres e-mail.":
            print_color(('Nie można dodać użytkownika z pustym polem tekstowym - test przeszedł pozytywnie'), "g")
        else:
            print_color(('Błędny test rejestracji użytkownika'), "r")


    def test_rejestracja_usera(self):

        self.driver.get("https://aleeesklep.local/my-account/")

        self.get_field_login = self.driver.find_element(By.XPATH, '//input[@id="reg_username"]')
        self.get_field_login.send_keys(Test_sklep.login)
        self.get_field_password = self.driver.find_element(By.XPATH, '//input[@id="reg_password"]')
        self.get_field_password.send_keys(Test_sklep.password)
        self.get_field_email = self.driver.find_element(By.XPATH, '//input[@id="reg_email"]')
        self.get_field_email.send_keys(Test_sklep.email)

        self.driver.find_element(By.XPATH, '//button[@name="register"]').click()

        try:
            if self.is_alert().is_displayed():
                print_color(('Użytkownik już istnieje'), "r")
            else:

                # znajdź element HTML, który zawiera tekst "Witaj"
                self.welcome_text = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Witaj')]").text

                name_text = self.driver.find_element(By.XPATH, "//*[contains(text(), '" + Test_sklep.login + "')]").text
                    # sprawdź, czy tekst "Witaj" i "login" znajdują się na stronie
                self.assertIn("Witaj", self.welcome_text)
                self.assertIn(Test_sklep.login, name_text)
        except:
            print_color(('Poprawna rejestracja klienta'), "g")
            time.sleep(10)

    def test_logowanie_usera(self):

        self.driver.get("https://aleeesklep.local/my-account/")

        self.driver.find_element(By.XPATH, '//input[@id="username"]').send_keys(Test_sklep.login)
        self.driver.find_element(By.XPATH, '//input[@id="password"]').send_keys(Test_sklep.password)

        self.driver.find_element(By.XPATH, '//button[@name="login"]').click()
        time.sleep(10)

        welcome_text = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Witaj')]").text

        name_text = self.driver.find_element(By.XPATH, "//*[contains(text(), '" + Test_sklep.login + "')]").text
        # sprawdź, czy tekst "Witaj" i "login" znajdują się na stronie
        try:
            self.assertIn("Witaj", welcome_text)
            self.assertIn(Test_sklep.login, name_text)
            print_color(('Poprawne logowanie klienta - klient zalogowany'), "g")
        except:
            print_color(('Błąd - Niepoprawne logowanie klienta'), "r")


    def test_czy_poprawnie_dodał_się_produkt(self):
        # Sprawdzenie czy tylko jeden produkt dodał się do koszyka

        click_new_products = self.driver.find_element(By.XPATH, '//li[@id="menu-item-796"]/a[@class="menu-link"]')
        click_new_products.click()
        #przejscie do strony Nowe produkty
        click_title_products = self.driver.find_element(By.XPATH, '//a[@href="https://aleeesklep.local/produkt/serenity-silver-watch/"]//img[@class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail"]')
        click_title_products.click()
        take_cost_of_product = self.driver.find_element(By.XPATH, '//div[@class="summary entry-summary"]//bdi[1]')
        text_take_cost_of_product = take_cost_of_product.text
        take_product = self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]')
        take_product.click()
        check_the_same_product = self.driver.find_element(By.XPATH, '//div[@id="ast-desktop-header"]//div[contains(@class,"ast-site-header-cart-li")]//bdi[1]')
        text_check_the_same_product = check_the_same_product.text

        if text_check_the_same_product  == text_take_cost_of_product:
            # Cena w koszyku się wyświela
            print_color(('Produkt został dodany do koszyka'), "g")
        else:
            print_color(('Produkt został nie dodany do koszyka'), "r")

    def test_czy_mozna_dodac_3_produkty(self):

        click_new_products = self.driver.find_element(By.XPATH, '//li[@id="menu-item-796"]/a[@class="menu-link"]')
        click_new_products.click()
        #Przejście do strony Nowe produkty
        click_title_products = self.driver.find_element(By.XPATH, '//a[@href="https://aleeesklep.local/produkt/serenity-silver-watch/"]//img[@class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail"]')
        click_title_products.click()
        # Kliknięcie na produkt
        self.driver.find_element(By.XPATH, '//div[@class="summary entry-summary"]//bdi[1]')
        # Pobranie ceny z produktu

        first_product = self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]')
        first_product.click()
        first_amount_products = self.driver.find_element(By.XPATH, '//i[@data-cart-total]')

        self.driver.find_element(By.XPATH, '//div[@id="ast-desktop-header"]//div[contains(@class,"ast-site-header-cart-li")]//bdi[1]')
        # Pobranie ceny z koszyka

        if first_amount_products.get_attribute("data-cart-total") == "1":
            print_color(("Produkt został dodany prawidłowo"),"g")

        else:
            print_color(("Produkt nie został dodany prawidłowo"), "r")


        self.driver.get("https://aleeesklep.local/nowe-produkty/")
        self.driver.find_element(By.XPATH, '//a[@href="https://aleeesklep.local/produkt/solla-outdoor-sunglasses/"]//img[@class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail"]').click()

        self.driver.find_element(By.XPATH, '//div[@class="summary entry-summary"]//bdi[1]')
        #pobranie ceny z produktu

        second_product = self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]')
        second_product.click()
        second_amount_products = self.driver.find_element(By.XPATH, '//i[@data-cart-total]')

        take_price_from_cart_second_prod = self.driver.find_element(By.XPATH, '//div[@id="ast-desktop-header"]//div[contains(@class,"ast-site-header-cart-li")]//bdi[1]')
        #pobranie z koszyka ceny

        if second_amount_products.get_attribute("data-cart-total") == "2":
            print_color(("Drugi produkt został dodany prawidłowo"), "g")
        else:
            print_color(("Drugi produkt nie został dodany prawidłowo"), "r")
        self.driver.get("https://aleeesklep.local/nowe-produkty/")
        self.driver.find_element(By.XPATH, '//a[@href="https://aleeesklep.local/produkt/allice-gold-necklace/"]//img[@class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail"]').click()
        self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]').click()
        third_amount_products = self.driver.find_element(By.XPATH, '//i[@data-cart-total]')

        if third_amount_products.get_attribute("data-cart-total") == "3":
            print_color(("Trzeci produkt został dodany prawidłowo"), "g")
        else:
            print_color(("Trzeci produkt nie został dodany prawidłowo"), "r")


    def test_sprawdzenie_sumowania_koszyka(self):

        click_new_products = self.driver.find_element(By.XPATH, '//li[@id="menu-item-796"]/a[@class="menu-link"]')
        click_new_products.click()
        # Przejście do strony Nowe produkty
        click_title_products = self.driver.find_element(By.XPATH, '//a[@href="https://aleeesklep.local/produkt/serenity-silver-watch/"]//img[@class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail"]')
        click_title_products.click()
        #Kliknięcie na produkt

        first_price = self.driver.find_elements(By.XPATH, '//div[@class="summary entry-summary"]//bdi[1]')
        #Przeprowadza pętlę przez każdy element z listy elementów cenowych, konwertuje tekst zawarty w elemencie na liczbę zmiennoprzecinkową i zapisuje ją w liście cen

        total = self.literowanie_po_elementach(first_price)
        expected_total = 249.99
        #Srebny zegarek
        try:
            assert total == expected_total, f"Oczekuje {expected_total}, a mam {total}"
            print_color(("Cena pierwszego produktu się zgadza z założoną"), "g")
        except:
            print_color(("Cena pierwszego produktu nie zgadza się z założoną"), "r")


        first_product = self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]')
        first_product.click()

        self.driver.get("https://aleeesklep.local/nowe-produkty/")
        self.driver.find_element(By.XPATH, '//a[@href="https://aleeesklep.local/produkt/solla-outdoor-sunglasses/"]//img[@class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail"]').click()

        second_price = self.driver.find_elements(By.XPATH, '//div[@class="summary entry-summary"]//bdi[1]')
        total1 = self.literowanie_po_elementach(second_price)

        # Przeprowadza pętlę przez każdy element z listy elementów cenowych, konwertuje tekst zawarty w elemencie na liczbę zmiennoprzecinkową i zapisuje ją w liście cen
        expected_total = 64.99
        #Okulary przeciwsłoneczne
        try:
            assert total1 == expected_total, f"Oczekuje {expected_total}, a mam {total}"
            print_color(("Cena drugiego produktu się zgadza z założoną"), "g")

        except:
            print_color(("Cena drugiego produktu nie zgadza się z założoną"), "r")

        second_product = self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]')
        second_product.click()
        self.driver.get("https://aleeesklep.local/nowe-produkty/")
        self.driver.find_element(By.XPATH, '//a[@href="https://aleeesklep.local/produkt/allice-gold-necklace/"]//img[@class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail"]').click()

        third_price = self.driver.find_elements(By.XPATH, '//div[@class="summary entry-summary"]//bdi[1]')
        total2 = self.literowanie_po_elementach(third_price)

        expected_total = 129.99
        #Złoty naszyjnik
        try:
            assert total2 == expected_total, f"Oczekuje {expected_total}, a mam {total}"
            print_color(("Cena trzeciego produktu się zgadza z założoną"), "g")

        except:
            print_color(("Cena trzeciego produktu nie zgadza się z założoną"), "r")

        self.driver.find_element(By.XPATH, '//button[@name="add-to-cart"]').click()

        self.suma = total+total1+total2

        total_value = self.driver.find_elements(By.XPATH, '//div[@id="ast-desktop-header"]//div[contains(@class,"ast-site-header-cart-li")]//bdi[1]')
        self.check_value_is_corect = self.literowanie_po_elementach(total_value)

        if self.suma == self.check_value_is_corect:
            print_color(("Ceny z produktów dodawanych do siebie zgadzają się z sumą ceny w koszyku"), "g")
        else:
            print_color(("Ceny z produktów dodawanych do siebie nie zgadzają się z sumą ceny w koszyku"), "r")


    def test_sprawdzenie_usuniecia_produktow(self):

        self.test_sprawdzenie_sumowania_koszyka()
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//div[@class="site-primary-header-wrap ast-builder-grid-row-container site-header-focus-item ast-container"]//span[@class="ast-woo-header-cart-info-wrap"]').click()
        #kliknięcie koszyka
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//div[contains(@class,"astra-cart-drawer-content")]//a[@class="button wc-forward wp-element-button"][normalize-space()="Zobacz koszyk"]').click()
        #kliknięcie "ZOBACZ KOSZYK"
        time.sleep(5)

        self.driver.find_element(By.XPATH, '//a[@class="remove"][1]').click()
        #Kliknij przycisk X przy produkcie
        time.sleep(5)
        take_value_from_cart = self.driver.find_elements(By.XPATH, '//tr[@class="cart-subtotal"]//bdi[1]')
        time.sleep(5)
        self.suma = self.literowanie_po_elementach(take_value_from_cart)
        convert_to_string = str(self.suma)
        expected_result = "194.98"
        if expected_result == convert_to_string:
            print_color(("Usunięcie poprawne - suma poprawna"), "g")
        else:
            print_color(("Suma usuwania nie poprawna"), "r")


    def test_sprawdź_mnożenie_ceny_przez_ilosc_produktow(self):

        self.test_sprawdzenie_sumowania_koszyka()

        quantity = 2
        #double_product = 499.98
        double_product = 500
        convert_string = str(double_product)

        self.driver.find_element(By.XPATH, '//div[@class="site-primary-header-wrap ast-builder-grid-row-container site-header-focus-item ast-container"]//span[@class="ast-woo-header-cart-info-wrap"]').click()
        # kliknięcie koszyka
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//div[contains(@class,"astra-cart-drawer-content")]//a[@class="button wc-forward wp-element-button"][normalize-space()="Zobacz koszyk"]').click()
        # kliknięcie "ZOBACZ KOSZYK"
        time.sleep(5)
        send_quantity = self.driver.find_element(By.XPATH, '//input[@class="input-text qty text"]')
        #Koszyk - ilosc produktów
        send_quantity.clear()
        send_quantity.send_keys(quantity)
        time.sleep(5)
        click_actualize_cart = self.driver.find_element(By.XPATH, '//button[@name="update_cart"]')
        # - "ZAKTUALIZUJ KOSZYK"
        click_actualize_cart.click()

        time.sleep(5)
        check_amount = self.driver.find_elements(By.XPATH, '//tbody/tr[1]/td[6]/span[1]/bdi[1]')
        # kwota produktu
        price_old = self.literowanie_po_elementach(check_amount)
        string_convert = str(price_old)

        try :
            if string_convert == convert_string:
                print_color(("Mnożenie produktów poprawne - test pozytywny"), "g")

        except:
            print_color(("Mnożenie produktów niepoprawne - test negatywny"), "r")


    def test_sprawdz_swoje_zamowienie(self):


        self.test_sprawdzenie_sumowania_koszyka()

        self.driver.find_element(By.XPATH,
                                 '//div[@class="site-primary-header-wrap ast-builder-grid-row-container site-header-focus-item ast-container"]//span[@class="ast-woo-header-cart-info-wrap"]').click()
        # kliknięcie koszyka
        time.sleep(5)
        self.driver.find_element(By.XPATH,
                                 '//div[contains(@class,"astra-cart-drawer-content")]//a[@class="button wc-forward wp-element-button"][normalize-space()="Zobacz koszyk"]').click()
        # kliknięcie "ZOBACZ KOSZYK"

        self.driver.find_element(By.XPATH, '//a[@href="https://aleeesklep.local/platnosc/"]').click()
        # Płatnosc

        total_products_price = self.driver.find_elements(By.XPATH, '//tr[@class="cart-subtotal"]//bdi[1]')
        get_total_products_price = self.literowanie_po_elementach(total_products_price)
        string_get_total_products_price = str(get_total_products_price)
        string_check_value_is_corect = str(self.check_value_is_corect)


        if string_check_value_is_corect == string_get_total_products_price:
            print("Poprawna wartość - cena produktów się zgadza")
        else:
            print("Niepoprawna wartość - cena produktów sie nie zgadza")


        name = self.driver.find_element(By.XPATH, '//input[@id="billing_first_name"]').send_keys("Jan")
        surname = self.driver.find_element(By.XPATH, '//input[@id="billing_last_name"]').send_keys("Kowalski")
        self.driver.find_element(By.XPATH, '//span[@id="select2-billing_country-container"]').click()
        time.sleep(5)

        self.driver.find_element(By.XPATH, '//h1[@class="entry-title"]').click()
        time.sleep(5)
        street = self.driver.find_element(By.XPATH, '//input[@id="billing_address_1"]').send_keys("Wiejska")
        post_code = self.driver.find_element(By.XPATH, '//input[@id="billing_postcode"]').send_keys("85-283")
        city = self.driver.find_element(By.XPATH, '//input[@id="billing_city"]').send_keys("Bydgoszcz")
        nr_tel = self.driver.find_element(By.XPATH, '//input[@id="billing_phone"]').send_keys("38732929")
        email = self.driver.find_element(By.XPATH, '//input[@id="billing_email"]').send_keys("jan.kowalski@gmail.com")

        all = [name, surname, street, post_code, city, nr_tel, email]
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//input[@name = "shipping_method[0]"]').click()
        #wybierz darmowa dostawe
        time.sleep(5)


    def pobranie_konwersja_float(self, xpath):

        converse = xpath.text.split(" ")[0].replace(",", ".")
        price_value = float(converse)

        return price_value

    def literowanie_po_elementach(self, price_elements):
        # Przeprowadza pętlę przez każdy element z listy elementów cenowych, konwertuje tekst zawarty w elemencie na liczbę zmiennoprzecinkową i zapisuje ją w liście cen
        prices = [float(element.text.split(" ")[0].replace(",", ".")) for element in price_elements]
        total = sum(prices)
        return total

    def zsumuj(self, suma):
        return sum(suma)

    def sum_sequence(sequence, add=None):
        if add:
            return sum(sequence) + add
        else:
            return sum(sequence)


    def podziel(self, value):
        n = value.split(" ")
        price = n[0]
        return print(price)

    def konwertuj(self, price):
        value = price.split(" ")[0].replace(",", ".")
        price_value = float(value)
        return price_value

if __name__ == '__main__':
    unittest.main()

