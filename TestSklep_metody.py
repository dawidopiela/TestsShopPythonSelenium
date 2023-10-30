import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from KolorTekst import print_color

class Test_sklep(unittest.TestCase):

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



    def test_sprawdzenie_tytulu_strony(self):

        try:
            title = self.driver.title
            assert 'aleeesklep' in title
            print_color(('Asercja - wyświetlenie tytułu - pozytywny'), "g")

        except Exception as e:
            print_color(('Asercja - wyświetlenie tytułu - negatywny', format(e)), "r")


    def test_istnieje_logo(self):


        logo = self.driver.find_element(By.XPATH, '//a[@class="custom-logo-link"][1]')
        self.assertTrue(logo.is_displayed())


    def test_menu_nawigacyjne(self):

        napis_stronaglowna = self.driver.find_element(By.XPATH, '//*[@id="menu-item-1032"]')
        text_strona_glowna = napis_stronaglowna.text
        napis_onas = self.driver.find_element(By.XPATH, '//li[@id="menu-item-1052"]')
        text_napis_onas = napis_onas.text
        napis_sukienki = self.driver.find_element(By.XPATH, '//*[@id="menu-item-708"]/a')
        text_napis_sukienki = napis_sukienki.text


        try:
            assert "Kolekcja 2023" in text_strona_glowna
            print("Napis Kolekcja 2023 się wyświetla")
        except:
            print("Napis Kolekcja 2023 się nie wyświetla")

        try:
            assert "O nas" in text_napis_onas
            print("Napis O nas się wyświetla")
        except:
            print("Napis O nas się nie wyświetla")

        try:
            assert "Sukienki" in text_napis_sukienki
            print("Napis Sukienki się wyświetla")
        except:
            print("Napis Sukienki się nie wyświetla")

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
        time.sleep(5)
        ikona_logowania = self.driver.find_element(By.XPATH, '//img[@class="avatar avatar-96 photo"]')
        ikona_logowania.click()

        self.driver.get("https://aleeesklep.local/my-account/")

        time.sleep(2)
        try:

            ikona_logowania = self.driver.find_element(By.XPATH, '//a[@aria-label="Account icon link"]')
            ikona_logowania.click()

            print("Ikona logowania występuje")

        except:
            print("Ikona logowania nie występuje")

        time.sleep(5)


    def test_sprawdzenie_wyświetlenia_opinii(self):

        self.driver.execute_script("window.scrollBy(0, 3500);")
        checkopion = self.driver.find_element(By.XPATH, '//div[@data-id="a155701"]//*[@class="elementor-testimonial-content"]')
        checkopionGetText = checkopion.text

        print(checkopionGetText)


        if checkopionGetText == 'Szybka dostawa. Szybka odpowiedź':
            print(f"Opinia {checkopionGetText} and  wyświetla się")
        else:
            print(f"Opinia {checkopionGetText} and  niewyświetla się")



    def test_registration_login(self):
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="ast-desktop-header"]//*[@class="account-icon"]')

        username = self.driver.find_element(By.XPATH, '//input[@id="user_login"]')
        username.send_keys("dawidadmin")
        password = self.driver.find_element(By.XPATH, '//input[@id="user_pass"]')
        password.send_keys("text")
        self.driver.find_element(By.XPATH, '//input[@name="wp-submit"]').click()



if __name__ == '__main__':
    unittest.main()

